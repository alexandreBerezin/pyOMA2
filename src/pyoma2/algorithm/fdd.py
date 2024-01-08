"""FREQUENCY DOMAIN DECOMPOSITION (FDD) ALGORITHM"""

import typing

import numpy as np
from pydantic import (  # controlla che i parametri passati siano quelli giusti
    validate_call,
)

from pyoma2.algorithm.data.result import (
    FDDResult,
)

# from .result import BaseResult
from pyoma2.algorithm.data.run_params import (
    FDDRunParams,
)
from pyoma2.functions import (  # noqa: F401
    FDD_funct,
    Gen_funct,
    SSI_funct,
    plot_funct,
    pLSCF_funct,
)

# from .run_params import BaseRunParams
from pyoma2.plot.Sel_from_plot import SelFromPlot

from .base import BaseAlgorithm


# METODI PER PLOT "STATICI" DOVE SI AGGIUNGONO?
# ALLA CLASSE BASE o A QUELLA SPECIFICA?
# =============================================================================
# BASIC FREQUENCY DOMAIN DECOMPOSITION
class FDD_algo(BaseAlgorithm[FDDRunParams, FDDResult]):
    RunParam = FDDRunParams
    ResultType = FDDResult
    method: typing.Literal["FDD"] = "FDD"

    def run(self) -> FDDResult:
        super()._pre_run()
        print(self.run_params)
        Y = self.data.T
        nxseg = self.run_params.nxseg
        method = self.run_params.method_SD
        # self.run_params.df = 1 / dt / nxseg

        freq, Sy = FDD_funct.SD_Est(Y, Y, self.dt, nxseg, method=method)
        Sval, Svec = FDD_funct.SD_svalsvec(Sy)

        # FIXME Non serve fare così, basta ritornare la classe result, 
        # poi sarà SingleSetup a salvarla

        # Fake result: FIXME return real FDDResult
        return FDDResult(
            freq=freq,
            Sy=Sy,
            S_val=Sval,
            S_vec=Svec,
        )

    @validate_call
    def mpe(self, sel_freq: float, DF: float = 0.1) -> typing.Any:
        super().mpe(sel_freq=sel_freq, DF=DF)

        self.run_params.sel_freq = sel_freq
        self.run_params.DF = DF
        Sy = self.result.Sy
        freq = self.result.freq

        # Get Modal Parameters
        Fn_FDD, Phi_FDD = FDD_funct.FDD_MPE(Sy, freq, sel_freq, DF=DF)

        # Save results
        # Qui è corretto perchè result esiste dopo che si è fatto il run()
        self.result.Fn = Fn_FDD
        self.result.Phi = Phi_FDD

    @validate_call
    def mpe_fromPlot(
        self, freqlim: typing.Optional[float] = None, DF: float = 0.1
    ) -> typing.Any:
        super().mpe_fromPlot(freqlim=freqlim)

        Sy = self.result.Sy
        freq = self.result.freq

        self.run_params.DF = DF

        # chiamare plot interattivo
        sel_freq = SelFromPlot(algo=self, freqlim=freqlim, plot="FDD")
        # FIXME qui dovrebbe essere
        self.run_params.sel_freq = sel_freq

        # e poi estrarre risultati
        Fn_FDD, Phi_FDD = FDD_funct.FDD_MPE(Sy, freq, sel_freq, DF=DF)

        # Save results
        # Qui è corretto perchè result esiste dopo che si è fatto il run()
        self.result.Fn = Fn_FDD
        self.result.Phi = Phi_FDD

    def plot_CMIF(self, *args, **kwargs) -> typing.Any:
        """Tobe implemented, plot for FDD, EFDD, FSDD
        Mode Identification Function (MIF)
        """
        if not self.result:
            raise ValueError("Run algorithm first")
        fig, ax = plot_funct.CMIF_plot(
            S_val=self.result.S_val,
            freq=self.result.freq,
            # freqlim=freqlim,
            # nSv=nSv
        )
        return fig, ax


# =============================================================================
# ENHANCED FREQUENCY DOMAIN DECOMPOSITION EFDD
class EFDD_algo(FDD_algo):
    method: typing.Literal["EFDD", "FSDD"] = "EFDD"

    @validate_call
    def mpe(
        self,
        sel_freq: float,
        method: typing.Literal[
            "EFDD", "FSDD"
        ],  # ATTENZIONE puo essere soltanto o "EFDD" o "FSDD"
        methodSy: str = "cor",  # o "cor" o "per"
        DF1: float = 0.1,
        DF2: float = 1.0,
        cm: int = 1,
        MAClim: float = 0.85,
        sppk: int = 3,
        npmax: int = 20,
    ) -> typing.Any:
        super().mpe(
            sel_freq=sel_freq,
            method=method,
            methodSy=methodSy,
            DF1=DF1,
            DF2=DF2,
            cm=cm,
            MAClim=MAClim,
            sppk=sppk,
            npmax=npmax,
        )

        Sy = self.result.Sy
        freq = self.result.freq

        Fn_FDD, Xi_FDD, Phi_FDD, forPlot = FDD_funct.EFDD_MPE(
            Sy,
            freq,
            self.dt,
            sel_freq,
            methodSy,
            method=method,
            DF1=DF1,
            DF2=DF2,
            cm=cm,
            MAClim=MAClim,
            sppk=sppk,
            npmax=npmax,
        )

        # Save results
        # Qui è corretto perchè result esiste dopo che si è fatto il run()
        self.result.Fn = Fn_FDD
        self.result.Xi = Xi_FDD
        self.result.Phi = Phi_FDD
        self.result.forPlot = forPlot

    @validate_call
    def mpe_fromPlot(
        self,
        method: typing.Literal["EFDD", "FSDD"],
        methodSy: str = "cor",
        DF1: float = 0.1,
        DF2: float = 1.0,
        cm: int = 1,
        MAClim: float = 0.85,
        sppk: int = 3,
        npmax: int = 20,
        freqlim: typing.Optional[float] = None,
    ) -> typing.Any:
        super().mpe_fromPlot(
            method=method,
            methodSy=methodSy,
            DF1=DF1,
            DF2=DF2,
            cm=cm,
            MAClim=MAClim,
            sppk=sppk,
            npmax=npmax,
            freqlim=freqlim,
        )

        Sy = self.result.Sy
        freq = self.result.freq

        # chiamare plot interattivo
        sel_freq = SelFromPlot(algo=self, freqlim=freqlim, plot="FDD")

        # e poi estrarre risultati
        Fn_FDD, Xi_FDD, Phi_FDD, forPlot = FDD_funct.EFDD_MPE(
            Sy,
            freq,
            self.dt,
            sel_freq,
            methodSy,
            method=method,
            DF1=DF1,
            DF2=DF2,
            cm=cm,
            MAClim=MAClim,
            sppk=sppk,
            npmax=npmax,
        )

        # Save results
        # Qui è corretto perchè result esiste dopo che si è fatto il run()
        self.result.Fn = Fn_FDD
        self.result.Xi = Xi_FDD
        self.result.Phi = Phi_FDD
        self.result.forPlot = forPlot

    def plot_FIT(self, *args, **kwargs) -> typing.Any:
        """Tobe implemented, plot for FDD, EFDD, FSDD
        Mode Identification Function (MIF)
        """
        if not self.result:
            raise ValueError("Run algorithm first")

        fig, ax = plot_funct.EFDD_FIT_plot(
            Fn=self.result.Fn,
            Xi=self.result.Xi,
            PerPlot = self.result.perPlot,
            # freqlim=freqlim,
        )
        return fig, ax

    def plot_mode(self, *args, **kwargs) -> typing.Any:
        """Tobe implemented, plot for FDD, EFDD, FSDD
        Mode Identification Function (MIF)
        """
        if not self.geometry1 or self.geometry2:
            raise ValueError("Definde the geometry first")

        if not self.result.Fn:
            raise ValueError("Run algorithm first")
        # argomenti plot mode:
        # modenumb: int # (da 1 a result.Phi.shape[1]+1)

        # fig, ax = 
        # return fig, ax

    def anim_mode(self, *args, **kwargs) -> typing.Any:
        """Tobe implemented, plot for FDD, EFDD, FSDD
        Mode Identification Function (MIF)
        """
        if not self.geometry2:
            raise ValueError("Definde the geometry (method 2) first")

        if not self.result:
            raise ValueError("Run algorithm first")

        # fig, ax = 
        # return fig, ax
    
# ------------------------------------------------------------------------------
# FREQUENCY SPATIAL DOMAIN DECOMPOSITION FSDD
class FSDD_algo(EFDD_algo):
    method: typing.Literal["EFDD", "FSDD"] = "FSDD"
