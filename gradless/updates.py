# AUTOGENERATED! DO NOT EDIT! File to edit: 02_updates.ipynb (unless otherwise specified).

__all__ = ['UpdateBase', 'StandardSPSA', 'ADAGRAD', 'ADAM', 'NADAM']

# Cell
import numpy
import scipy
from abc import ABC, abstractmethod

# Cell

class UpdateBase(ABC):
    """A helper class for constructing update rules"""
    @abstractmethod
    #This is the workhorse of the class
    def evaluate(self): pass


# Cell
class StandardSPSA(UpdateBase):
    """A standard gradient descent update."""
    def __init__(self):
        pass

    def evaluate(self,ghat, nu, t=0. ):

        return nu*ghat

# Cell
class ADAGRAD(UpdateBase):
    def __init__(self, eps=1e-8):
        self.eps=eps
        self.G_t=None

    def evaluate(self,ghat, nu, t=0. ):
        if self.G_t is None:
            self.G_t=numpy.zeros(ghat.shape)
        self.G_t+=ghat**2
        return nu*ghat/(self.G_t+self.eps)**.5

# Cell
class ADAM(UpdateBase):
    def __init__(self,beta1=.9, beta2=.999, eps=1e-8):
        self.beta1=beta1
        self.beta2=beta2
        self.eps=eps

        self.m_t=[0.]
        self.v_t=[0.]
    def evaluate(self,ghat, nu, t ):
        #Update the gradient histories
        self.m_t.append(self.beta1*self.m_t[-1]+(1-self.beta1)*ghat)
        self.v_t.append(self.beta2*self.v_t[-1]+(1-self.beta2)*ghat**2)

        #compute the bias corrections
        m_hat=self.m_t[-1]/(1.-self.beta1**t)
        v_hat=self.v_t[-1]/(1.-self.beta2**t)

        #compute the proposed step
        return nu*m_hat/(v_hat**.5+self.eps)

# Cell
class NADAM(UpdateBase):
    def __init__(self,beta1=.9, beta2=.999, eps=1e-8):
        self.beta1=beta1
        self.beta2=beta2
        self.eps=eps

        self.m_t=[0.]
        self.v_t=[0.]
    def evaluate(self,ghat, nu, t ):
        #Update the gradient histories
        self.m_t.append(self.beta1*self.m_t[-1]+(1-self.beta1)*ghat)
        self.v_t.append(self.beta2*self.v_t[-1]+(1-self.beta2)*ghat**2)


        if t>=2:
            m_hat=self.m_t[-1]/(1-self.beta1**(t-1))
        else:
            m_hat=0.
        v_hat=self.v_t[-1]/(1-self.beta2**t)


        part_1=(nu/(v_hat**.5+self.eps))
        part_2=self.beta1*m_hat
        part_3=(1-self.beta1)*ghat/(1-self.beta1**t)
        step=part_1*(part_2+part_3)
        return step