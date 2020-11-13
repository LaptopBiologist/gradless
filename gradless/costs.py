# AUTOGENERATED! DO NOT EDIT! File to edit: 03_models.ipynb (unless otherwise specified).

__all__ = ['ModelBase', 'Model', 'ELBO']

# Cell
import numpy
import scipy
import scipy.stats

from abc import ABC, abstractmethod

# Cell
class ModelBase(ABC):


    RV=None
    update_rvs=True
    @abstractmethod     #Require that all cost functions have the .evaluate method

    def evaluate(self): pass

    def sample_rvs(self):
        """This can be used to regenerate a random variable used by the cost function.
        It may be desirable hold some random variables constant during gradient evaluations, for example"""
        if self.RV is not None:
            self.z=self.RV.rvs()

#         raise NotImplementedError("Cost functions must included a boolean attribute 'update_rvs'")



# Cell
class Model(ModelBase):
    def __init__(self, cost, data, RV=None, update_rvs=False):

        self.cost=cost
        self.data=data
        self.RV=RV
        if self.RV is not None:
            self.z=self.sample_rvs()

        if RV is None:
            self.update_rvs=False
        else:
            assert type(update_rvs) is bool
            self.update_rvs=update_rvs
    def evaluate(self, theta):
        if self.data is None:
            return self.cost(theta)
        if self.RV is None:
            return self.cost(theta, self.data)
        else:
            return self.cost(theta, self.data, self.z)

# Cell


class ELBO(ModelBase):
    def __init__(self, evidence, data, param_num, log=True, update_rvs=True):
        self.cost=evidence
        self.data=data
        self.param_num=param_num
        self.update_rvs=True
        self.RV=scipy.stats.norm([0.]*param_num,[1.]*param_num)
        self.z=self.RV.rvs()
        self.log=log

    def evaluate(self, theta):
        mu=theta[:self.param_num]
        sd=2.**theta[self.param_num:]

        eps=mu+self.z*(sd)

        p=self.cost(eps, self.data)
        q=scipy.stats.norm.logpdf(eps, mu,sd).sum()
        if self.log==True:
            return numpy.log10(-(p-q))
        else:
            return -(p-q)
#     def up