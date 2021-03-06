import numpy as np
import sympy as sp
from scipy.integrate import quad

from CubicEOS import CubicEOS
from Properties import Props
from compounds import MixtureProp
from constants import R_IG
from polyEqSolver import solve_cubic

eos_options = {
    "van der Waals (1890)": "van_der_waals_1890",
    "Redlich and Kwong (1949)": "redlich_and_kwong_1949",
    "Wilson (1964)": "wilson_1964",
    "Soave (1972)": "soave_1972",
    "Peng and Robinson (1976)": "peng_and_robinson_1976",
    # "Schmidt and Wenzel (1979)": "schmidt_and_wenzel_1979", # conferir regra de mistura para esse
    "Péneloux, et al. (1982)": "peneloux_et_al_1982",
    "Patel and Teja (1982)": "patel_and_teja_1982",
    "Adachi, et al. (1983)": "adachi_et_al_1983",
    "Soave (1984)": "soave_1984",
    "Adachi, et al. (1985)": "adachi_et_al_1985",
    "Stryjek and Vera (1986)": "stryjek_and_vera_1986",
    "Twu, et al. (1995)": "twu_et_al_1995",
    "Ahlers-Gmehling (2001)": "ahlers_gmehling_2001",
    "Gasem, et al. PR modification (2001)": "gasem_et_al_pr_2001",
    "Gasem, et al. Twu modificaton (2001)": "gasem_et_al_twu_2001",
    "Gasem, et al.(2001)": "gasem_et_al_2001",
}


class EOS(CubicEOS):
    def __init__(self, mix: MixtureProp, k, eos):
        super().__init__()

        self.mix = mix
        self.y = np.atleast_1d(self.mix.y)
        self.k = k
        self.n = self.mix.n

        self.symb_N = sp.symbols("N", real=True, positive=True)
        self.symb_Ns = sp.symbols("N:{}".format(self.n), real=True, positive=True)

        self.symb_y = sp.symbols("y", real=True, positive=True)
        self.symb_ys = sp.symbols("y:{}".format(self.n), real=True, positive=True)

        self.symb_thetam = 0
        self.symb_bm = 0
        self.symb_epsilonm = 0
        self.symb_deltam = 0

        self.eosDisplayName = eos
        self.eosValue = eos_options[self.eosDisplayName]

        self.Zcs = np.zeros(self.n)
        self.Vcs = np.zeros(self.n)
        self.Pcs = np.zeros(self.n)
        self.Tcs = np.zeros(self.n)
        self.omegas = np.zeros(self.n)

        for i in range(self.n):
            self.Zcs[i] = self.mix.substances[i].Zc
            self.Vcs[i] = self.mix.substances[i].Vc
            self.Tcs[i] = self.mix.substances[i].Tc
            self.Pcs[i] = self.mix.substances[i].Pc
            self.omegas[i] = self.mix.substances[i].omega

        self._initialize()
        self._computeParameters()

    def _initialize(self):

        if self.eosValue == "van_der_waals_1890":
            thetas = []
            self.b = 0
            for i in range(self.n):
                self.b += (0.125 / (self.Pcs[i] / (R_IG * self.Tcs[i]))) * self.y[i]
                thetas.append(0.42188 * (R_IG * self.Tcs[i]) ** 2 / self.Pcs[i])

            self._calculate_theta_mixture(thetas)
            self.delta = 0.0
            self.epsilon = 0.0

        elif self.eosValue == "redlich_and_kwong_1949":
            thetas = []
            self.b = 0
            for i in range(self.n):
                self.b += (0.08664 / (self.Pcs[i] / (R_IG * self.Tcs[i]))) * self.y[i]
                thetas.append(
                    (0.42748 * (R_IG * self.Tcs[i]) ** 2 / self.Pcs[i])
                    / (self.T / self.Tcs[i]) ** 0.5
                )

            self._calculate_theta_mixture(thetas)
            self.delta = self.b
            self.epsilon = 0.0

        elif self.eosValue == "wilson_1964":
            thetas = []
            self.b = 0
            for i in range(self.n):
                self.b += (0.08664 / (self.Pcs[i] / (R_IG * self.Tcs[i]))) * self.y[i]
                a = 0.42748 * (R_IG * self.Tcs[i]) ** 2 / self.Pcs[i]
                alpha = (self.T / self.Tcs[i]) * (
                    1
                    + (1.57 + 1.62 * self.omegas[i])
                    * (1.0 / (self.T / self.Tcs[i]) - 1.0)
                )
                thetas.append(a * alpha)

            self._calculate_theta_mixture(thetas)
            self.delta = self.b
            self.epsilon = 0.0

        elif self.eosValue == "soave_1972":
            thetas = []
            self.b = 0
            for i in range(self.n):
                self.b += (0.08664 / (self.Pcs[i] / (R_IG * self.Tcs[i]))) * self.y[i]
                a = 0.42748 * (R_IG * self.Tcs[i]) ** 2 / self.Pcs[i]
                alpha = (
                    1.0
                    + (0.48 + 1.574 * self.omegas[i] - 0.176 * self.omegas[i] ** 2)
                    * (1.0 - (self.T / self.Tcs[i]) ** 0.5)
                ) ** 2
                thetas.append(a * alpha)

            self._calculate_theta_mixture(thetas)
            self.delta = self.b
            self.epsilon = 0.0

        elif self.eosValue == "peng_and_robinson_1976":

            thetas = []
            self.b = 0
            for i in range(self.n):
                self.b += self.y[i] * (0.07780 / (self.Pcs[i] / (R_IG * self.Tcs[i])))
                self.symb_bm += (self.symb_ys[i]) * (
                    0.07780 / (self.Pcs[i] / (R_IG * self.Tcs[i]))
                )
                _tmpthetas = (
                    (
                        1.0
                        + (
                            0.37464
                            + 1.54226 * self.omegas[i]
                            - 0.2699 * self.omegas[i] ** 2
                        )
                        * (1.0 - (self.T / self.Tcs[i]) ** 0.5)
                    )
                    ** 2
                ) * (0.45724 * (R_IG * self.Tcs[i]) ** 2 / self.Pcs[i])
                thetas.append(_tmpthetas)

            self._calculate_theta_mixture(thetas)
            self._symb_calculate_theta_mixture(thetas)
            self.delta = 2 * self.b
            self.symb_deltam = 2 * self.symb_bm
            self.epsilon = -self.b * self.b
            self.symb_epsilonm = -self.symb_bm ** 2

        elif self.eosValue == "peneloux_et_al_1982":
            thetas = []
            self.b = 0
            c = 0
            for i in range(self.n):
                a = 0.42748 * (R_IG * self.Tcs[i]) ** 2 / self.Pcs[i]
                c += (
                    0.40768
                    * (R_IG * self.Tcs[i] / self.Pcs[i])
                    * (0.00385 + 0.08775 * self.omegas[i])
                ) * self.y[i]
                self.b += (0.08664 / (self.Pcs[i] / (R_IG * self.Tcs[i]))) * self.y[i]
                alpha = (
                    1.0
                    + (0.48 + 1.574 * self.omegas[i] - 0.176 * self.omegas[i] ** 2)
                    * (1.0 - (self.T / self.Tcs[i]) ** 0.5)
                ) ** 2
                thetas.append(a * alpha)
            self.b = self.b - c
            self._calculate_theta_mixture(thetas)
            self.delta = self.b + 2 * c
            self.epsilon = c * (self.b + c)

        elif self.eosValue == "patel_and_teja_1982":
            thetas = []
            self.b = 0
            c = 0
            for i in range(self.n):
                F = 0.45241 + 1.30982 * self.omegas[i] - 0.295937 * self.omegas[i] ** 2
                zeta_c = (
                    0.32903
                    - 0.076799 * self.omegas[i]
                    + 0.0211947 * self.omegas[i] ** 2
                )
                r = np.atleast_1d(
                    solve_cubic(1, 2 - 3 * zeta_c, 3 * zeta_c ** 2, -zeta_c ** 3)
                )
                omega_b = np.min(r[r >= 0])
                omega_c = 1 - 3 * zeta_c
                omega_a = (
                    3 * zeta_c ** 2
                    + 3 * (1 - 2 * zeta_c) * omega_b
                    + omega_b ** 2
                    + 1
                    - 3 * zeta_c
                )
                c += self.y[i] * omega_c * R_IG * self.Tcs[i] / self.Pcs[i]
                self.b += self.y[i] * omega_b * R_IG * self.Tcs[i] / self.Pcs[i]
                alpha = (1 + F * (1 - (self.T / self.Tcs[i]) ** 0.5)) ** 2
                a = omega_a * (R_IG * self.Tcs[i]) ** 2 / self.Pcs[i]
                thetas.append(a * alpha)
            self._calculate_theta_mixture(thetas)
            self.delta = self.b + c
            self.epsilon = -self.b * c

        elif self.eosValue == "adachi_et_al_1983":
            thetas = []
            self.b = 0
            c = 0
            b1, b2, b3 = 0, 0, 0
            for i in range(self.n):
                b1 += self.y[i] * (
                    R_IG
                    * self.Tcs[i]
                    * (
                        0.08974
                        - 0.03452 * self.omegas[i]
                        + 0.00330 * self.omegas[i] ** 2
                    )
                    / self.Pcs[i]
                )
                b2 += self.y[i] * (
                    R_IG
                    * self.Tcs[i]
                    * (
                        0.03686
                        + 0.00405 * self.omegas[i]
                        - 0.01073 * self.omegas[i] ** 2
                        + 0.00157 * self.omegas[i] ** 3
                    )
                    / self.Pcs[i]
                )
                b3 += self.y[i] * (
                    R_IG
                    * self.Tcs[i]
                    * (
                        0.154
                        + 0.14122 * self.omegas[i]
                        - 0.00272 * self.omegas[i] ** 2
                        - 0.00484 * self.omegas[i] ** 3
                    )
                    / self.Pcs[i]
                )

                a = (
                    (R_IG * self.Tcs[i]) ** 2
                    * (
                        0.44869
                        + 0.04024 * self.omegas[i]
                        + 0.01111 * self.omegas[i] ** 2
                        - 0.00576 * self.omegas[i] ** 3
                    )
                    / self.Pcs[i]
                )
                alpha = (
                    1
                    + (0.407 + 1.3787 * self.omegas[i] - 0.2933 * self.omegas[i] ** 2)
                    * (1.0 - (self.T / self.Tcs[i]) ** 0.5)
                ) ** 2
                thetas.append(a * alpha)

            self.b = b1
            self._calculate_theta_mixture(thetas)
            self.delta = b3 - b2
            self.epsilon = -b2 * b3

        elif self.eosValue == "soave_1984":
            thetas = []
            self.b = 0
            self.epsilon = 0
            for i in range(self.n):
                self.b += (0.08333 / (self.Pcs[i] / (R_IG * self.Tcs[i]))) * self.y[i]
                self.epsilon += (
                    0.001736 / (self.Pcs[i] / (R_IG * self.Tcs[i])) ** 2 * self.y[i]
                )
                a = 0.42188 * (R_IG * self.Tcs[i]) ** 2 / self.Pcs[i]
                alpha = (
                    1.0
                    + (
                        0.4998
                        + 1.5928 * self.omegas[i]
                        - 0.19563 * self.omegas[i] ** 2
                        + 0.025 * self.omegas[i] ** 3
                    )
                    * (1.0 - (self.T / self.Tcs[i]) ** 0.5)
                ) ** 2
                thetas.append(a * alpha)

            self._calculate_theta_mixture(thetas)
            self.delta = self.b

        elif self.eosValue == "adachi_et_al_1985":
            thetas = []
            self.b = 0
            c = 0
            for i in range(self.n):
                a = (
                    (R_IG * self.Tcs[i]) ** 2
                    * (
                        0.43711
                        + 0.02366 * self.omegas[i]
                        + 0.10538 * self.omegas[i] ** 2
                        + 0.10164 * self.omegas[i] ** 3
                    )
                    / self.Pcs[i]
                )
                self.b += self.y[i] * (
                    (R_IG * self.Tcs[i])
                    * (
                        0.08779
                        - 0.02181 * self.omegas[i]
                        - 0.06708 * self.omegas[i] ** 2
                        + 0.10617 * self.omegas[i] ** 3
                    )
                    / self.Pcs[i]
                )
                c += self.y[i] * (
                    (R_IG * self.Tcs[i])
                    * (
                        0.0506
                        + 0.04184 * self.omegas[i]
                        + 0.16413 * self.omegas[i] ** 2
                        - 0.03975 * self.omegas[i] ** 3
                    )
                    / self.Pcs[i]
                )
                alpha = (
                    1
                    + (
                        0.4406
                        + 1.7039 * self.omegas[i]
                        - 1.729 * self.omegas[i] ** 2
                        + 0.9929 * self.omegas[i] ** 3
                    )
                    * (1 - (self.T / self.Tcs[i]) ** 0.5)
                ) ** 2
                thetas.append(a * alpha)

            self._calculate_theta_mixture(thetas)
            self.delta = 2 * c
            self.epsilon = -c ** 2

        elif self.eosValue == "stryjek_and_vera_1986":

            thetas = []
            self.b = 0
            for i in range(self.n):
                self.b += self.y[i] * (0.07780 / (self.Pcs[i] / (R_IG * self.Tcs[i])))
                self.symb_bm += (self.symb_ys[i]) * (
                    0.07780 / (self.Pcs[i] / (R_IG * self.Tcs[i]))
                )
                k0 = (
                    0.378893
                    + 1.48971530 * self.omegas[i]
                    - 0.17131848 * self.omegas[i] ** 2
                    + 0.0196554 * self.omegas[i] ** 3
                )
                k1 = 0

                name = self.mix.substances[i].Name
                if name == "hexadecane":
                    k1 = 0.02665
                elif name == "hexane":
                    k1 = 0.05104
                elif name == "cyclohexane":
                    k1 = 0.07023
                elif name == "methane":
                    k1 = -0.00159
                elif name == "benzene":
                    k1 = 0.07019

                Tr = self.T / self.Tcs[i]
                k = k0 + k1 * (1 + Tr) * (0.7 - Tr)

                _tmpthetas = (
                    (1.0 + (k) * (1.0 - (self.T / self.Tcs[i]) ** 0.5)) ** 2
                ) * (0.45724 * (R_IG * self.Tcs[i]) ** 2 / self.Pcs[i])
                thetas.append(_tmpthetas)

            self._calculate_theta_mixture(thetas)
            self._symb_calculate_theta_mixture(thetas)
            self.delta = 2 * self.b
            self.symb_deltam = 2 * self.symb_bm
            self.epsilon = -self.b * self.b
            self.symb_epsilonm = -self.symb_bm ** 2

        elif self.eosValue == "twu_et_al_1995":
            thetas = []
            self.b = 0
            for i in range(self.n):
                self.b += (
                    self.y[i] * (R_IG * self.Tcs[i]) * 0.0777960739039 / self.Pcs[i]
                )
                a = (R_IG * self.Tcs[i]) ** 2 * 0.457235528921 / self.Pcs[i]
                alpha0 = (self.T / self.Tcs[i]) ** (
                    -0.171813
                ) * 2.718281828459045235360 ** (
                    0.125283 * (1 - (self.T / self.Tcs[i]) ** 1.77634)
                )
                alpha1 = (self.T / self.Tcs[i]) ** (
                    -0.607352
                ) * 2.718281828459045235360 ** (
                    0.511614 * (1 - (self.T / self.Tcs[i]) ** 2.20517)
                )
                alpha = alpha0 + self.omegas[i] * (alpha1 - alpha0)
                thetas.append(a * alpha)

            self._calculate_theta_mixture(thetas)
            self.delta = self.b * 2
            self.epsilon = -self.b ** 2

        elif self.eosValue == "ahlers_gmehling_2001":
            thetas = []
            self.b = 0
            c = 0
            for i in range(self.n):
                a = 0.45724 * (R_IG * self.Tcs[i]) ** 2 / self.Pcs[i]
                alpha = (
                    1.0
                    + (
                        0.37464
                        + 1.54226 * self.omegas[i]
                        - 0.2699 * self.omegas[i] ** 2
                    )
                    * (1.0 - (self.T / self.Tcs[i]) ** 0.5)
                ) ** 2
                gamma = 246.78 * self.Zcs[i] ** 2 - 107.21 * self.Zcs[i] + 12.67
                n = -74.458 * self.Zcs[i] + 26.966
                beta = 0.35 / (
                    0.35 + (n * np.abs((self.T / self.Tcs[i]) - alpha)) ** gamma
                )
                cc = (
                    (0.3074 - self.Zcs[i]) * R_IG * (self.T / self.Tcs[i]) / self.Pcs[i]
                )
                c += (cc * beta) * self.y[i]
                self.b += self.y[i] * 0.07780 / (self.Pcs[i] / (R_IG * self.Tcs[i]))
                thetas.append(a * alpha)

            self._calculate_theta_mixture(thetas)
            self.b = self.b - c
            self.delta = self.b * 2
            self.epsilon = -self.b * self.b + 4 * self.b * c - 2 * c ** 2

        elif self.eosValue == "gasem_et_al_pr_2001":
            thetas = []
            self.b = 0
            for i in range(self.n):
                a = 0.45724 * (R_IG * self.Tcs[i]) ** 2 / self.Pcs[i]
                self.b += self.y[i] * 0.07780 / (self.Pcs[i] / (R_IG * self.Tcs[i]))
                alpha = (
                    1.0
                    + (
                        0.386590
                        + 1.50226 * self.omegas[i]
                        - 0.1687 * self.omegas[i] ** 2
                    )
                    * (1.0 - (self.T / self.Tcs[i]) ** 0.5)
                ) ** 2
                thetas.append(a * alpha)

            self._calculate_theta_mixture(thetas)
            self.delta = 2 * self.b
            self.epsilon = -self.b ** 2

        elif self.eosValue == "gasem_et_al_twu_2001":
            thetas = []
            self.b = 0
            for i in range(self.n):
                a = 0.45724 * (R_IG * self.Tcs[i]) ** 2 / self.Pcs[i]
                self.b += self.y[i] * 0.07780 / (self.Pcs[i] / (R_IG * self.Tcs[i]))
                alpha0 = (self.T / self.Tcs[i]) ** (
                    -0.207176
                ) * 2.718281828459045235360 ** (
                    0.092099 * (1 - (self.T / self.Tcs[i]) ** 1.94800)
                )
                alpha1 = (self.T / self.Tcs[i]) ** (
                    -0.502297
                ) * 2.718281828459045235360 ** (
                    0.603486 * (1 - (self.T / self.Tcs[i]) ** 2.09626)
                )
                alpha = alpha0 + self.omegas[i] * (alpha1 - alpha0)
                thetas.append(a * alpha)

            self._calculate_theta_mixture(thetas)
            self.delta = 2 * self.b
            self.epsilon = -self.b ** 2

        elif self.eosValue == "gasem_et_al_2001":
            thetas = []
            self.b = 0
            for i in range(self.n):
                a = 0.45724 * (R_IG * self.Tcs[i]) ** 2 / self.Pcs[i]
                self.b += self.y[i] * 0.07780 / (self.Pcs[i] / (R_IG * self.Tcs[i]))
                A = 2.0
                B = 0.836
                C = 0.134
                D = 0.508
                E = -0.0467

                Tr = self.T / self.Tcs[i]
                w = self.omegas[i]
                alpha = 2.718281828459045235360 ** (
                    (A + B * Tr) * (1.0 - Tr ** (C + w * (D + E * w)))
                )

                thetas.append(a * alpha)

            self._calculate_theta_mixture(thetas)
            self.delta = 2 * self.b
            self.epsilon = -self.b ** 2

        else:
            raise ValueError("Equation of state doesn't exists in the current database")

        # ========= END OF self._initialize() ===============

    def _calculate_theta_mixture(self, thetas):
        self.theta = 0
        for i in range(self.n):
            inner_sum = 0
            for j in range(self.n):
                inner_sum += (
                    self.y[i]
                    * self.y[j]
                    * sp.sqrt(thetas[i] * thetas[j])
                    * (1 - self.k[i][j])
                )
            self.theta += inner_sum

    def _symb_calculate_theta_mixture(self, thetas):
        for i in range(self.n):
            inner_sum = 0
            for j in range(self.n):
                inner_sum += (
                    (self.symb_ys[i])
                    * (self.symb_ys[j])
                    * sp.sqrt(thetas[i] * thetas[j])
                    * (1 - self.k[i][j])
                )
            self.symb_thetam += inner_sum

    def getAllProps(
        self, Tref: float, T: float, Pref: float, P: float
    ) -> (Props, Props):
        log = ""

        zs = self.getZfromPT(P, T)
        zliq, zvap = np.min(zs), np.max(zs)
        vliq, vvap = zliq * R_IG * T / P, zvap * R_IG * T / P

        avgMolWt = self.mix.getMolWt()
        if avgMolWt:
            rholiq, rhovap = avgMolWt * 1e-3 / vliq, avgMolWt * 1e-3 / vvap
        else:
            rholiq, rhovap = 0, 0

        if self.mix.hasCp():
            igprops = self.mix.getIGProps(Tref, T, Pref, P)
            log += self.mix.getCpLog(Tref, T)
            pliq, pvap = self.getCpHSGUA(Tref, T, Pref, P)
        else:
            igprops = 0
            pliq, pvap = 0, 0
            log += "Couldn't calculate properties: missing Cp paramaters"

        fl, fv = self.getFugacity(P, T, vliq, zliq), self.getFugacity(P, T, vvap, zvap)

        retPropsliq, retPropsvap = Props(), Props()
        retPropsliq.Z, retPropsvap.Z = zliq, zvap
        retPropsliq.V, retPropsvap.V = vliq, vvap
        retPropsliq.rho, retPropsvap.rho = rholiq, rhovap
        retPropsliq.P, retPropsvap.P = P, P
        retPropsliq.T, retPropsvap.T = T, T
        retPropsliq.Fugacity, retPropsvap.Fugacity = fl, fv
        retPropsliq.IGProps, retPropsvap.IGProps = igprops, igprops
        retPropsliq.Props, retPropsvap.Props = pliq, pvap
        retPropsliq.log, retPropsvap.log = log, log

        return retPropsliq, retPropsvap

    def getCpHSGUA(self, Tref: float, T: float, Pref: float, P: float):
        zs = self.getZfromPT(P, T)
        zsref = self.getZfromPT(Pref, Tref)

        zliq, zvap = np.min(zs), np.max(zs)
        zliqref, zvapref = np.min(zsref), np.max(zsref)

        vliq, vvap = zliq * R_IG * T / P, zvap * R_IG * T / P
        vliqref, vvapref = zliqref * R_IG * Tref / Pref, zvapref * R_IG * Tref / Pref

        igprop = self.mix.getIGProps(
            Tref, T, Pref, P
        )  # make sure that mixture can handle single substances

        ddp_liq = self.getDeltaDepartureProps(
            Pref, Tref, vliqref, zliqref, P, T, vliq, zliq
        )
        ddp_vap = self.getDeltaDepartureProps(
            Pref, Tref, vvapref, zvapref, P, T, vvap, zvap
        )
        pliq = igprop.subtract(ddp_liq)
        pvap = igprop.subtract(ddp_vap)

        return pliq, pvap

    # lazy code, it can be improved a lot
    def getPhi_i(self, i: int, _P: float, _T: float, _V: float, _Z: float) -> float:

        symb_Z = self.V / (self.V - self.symb_bm) - self.V * (
            self.symb_thetam / (R_IG * self.T)
        ) / (
            (self.V - self.symb_bm)
            * (self.V ** 2 + self.symb_deltam * self.V + self.symb_epsilonm)
        )
        integrand = (sp.diff(symb_Z, self.symb_ys[i]) - 1) / self.V

        for j in range(self.n):
            integrand = integrand.subs(self.symb_ys[j], self.y[j])

        integrand_num = sp.lambdify(
            [self.V, self.P, self.T], integrand, modules="numpy"
        )

        res = quad(integrand_num, _V, np.inf, args=(_P, _T))[0] - np.log(_Z)
        a = np.exp(res)

        return np.exp(res)

    def _getPb_initial_guess(self, _T: float, _x) -> float:
        _x = np.atleast_1d(_x)
        pb = float(
            np.sum(
                _x
                * self.Pcs
                * np.exp(5.373 * (1 + self.omegas) * (1.0 - self.Tcs / _T))
            )
        )
        return pb

    def getBubblePointPressure(self, _T: float, x) -> float:
        assert np.sum(x) == 1

        x = np.atleast_1d(x)
        Pb = self._getPb_initial_guess(_T, x)
        k = np.log(self.Pcs / Pb) + 5.373 * (1.0 + self.omegas) * (1.0 - self.Tcs / _T)

        y = x * k / np.sum(x * k)

        tol = 1e-8
        err = 1000
        ite = 0
        kmax = 10000

        y = np.full(self.n, 1.0 / self.n)
        phivap = np.empty(self.n, dtype=float)
        philiq = np.empty(self.n, dtype=float)

        while err > tol and ite < kmax:
            ite += 1

            vapmix = MixtureProp([s for s in self.mix.substances], y)
            liqmix = MixtureProp([s for s in self.mix.substances], x)

            vapeos = EOS(vapmix, self.k, self.eosDisplayName)
            liqeos = EOS(liqmix, self.k, self.eosDisplayName)

            zvap = np.max(vapeos.getZfromPT(Pb, _T))
            zliq = np.min(liqeos.getZfromPT(Pb, _T))

            vvap, vliq = R_IG * _T * zvap / Pb, R_IG * _T * zliq / Pb

            for i in range(self.n):
                phivap[i] = vapeos.getPhi_i(i, Pb, _T, vvap, zvap)
                philiq[i] = liqeos.getPhi_i(i, Pb, _T, vliq, zliq)

            k = philiq / phivap
            y = x * k
            yt = np.sum(y)
            err = np.abs(yt - 1.0)

        print(Pb)
        print(y)
