# AUTOGENERATED! DO NOT EDIT! File to edit: 04_gradient.ipynb (unless otherwise specified).

__all__ = ['GradientBase', 'SPSAGradient']

# Cell
import numpy
import scipy
from abc import ABC, abstractmethod

# Cell

class GradientBase(ABC):
    """A helper class that provides a standard means to create
    classes to provide gradients or their approximations to GradientDescent."""
    @abstractmethod
    #This is the workhorse of the class
    def evaluate(self): pass


# Cell
class SPSAGradient(GradientBase):
    """A class for computing the SPSA gradient estimate."""
    def __init__(self, param_subsets=None,fraction=None, cost=None):
        self.cost=cost
        self.param_subsets=param_subsets
        if self.param_subsets is not None:
            self.param_subsets=numpy.array(self.param_subsets)
            self.subsets=set(list(param_subsets))

    def set_cost(self, cost):
        self.cost=cost

    def evaluate(self, theta, c_k, gradient_reps=1, update_rvs=False):
        """Inputs
        1. theta - A 1-D numpy array of model parameters
        2. c_k - A step size that may be used in the gradient evaluation
        3. gradient_reps - The number of times to evaluate the gradient
            (multiple evaluations will be averaged)
        4. update_rvs - Whether regenerated random variables stored in
            the cost function after each gradient evaluation

            Returns an array gradient estimates the same size as theta

        """

#         assert len(theta)==len(self.)
        #If no subsets were defined, then now we'll define all model parameters as one set
        assert self.cost is not None

        if self.param_subsets is None:
            self.param_subsets=numpy.zeros(theta.shape[0])
            self.subsets=set(list(self.param_subsets))
        #evaluate the gradient separately for different groups of parameters
        grad_list=[]
        for rep in range(gradient_reps):
            if update_rvs==True:     #Regenerate the random numbers in the cost with each gradient
                self.cost.sample_rvs()
            ghat=numpy.zeros(theta.shape)
            for s in self.subsets:

                param_filter=self.param_subsets==s

                ghat+=self.SPSA( theta, c_k, param_filter)
            grad_list.append(ghat)
        if gradient_reps==1:
            return grad_list[0]
        else: #We need to average
#             print (grad_list)
#             print ( numpy.mean(grad_list,0))
#             print (jabber)
            return numpy.mean(grad_list,0)

    def SPSA(self, theta, ck, param_ind):
        """ Inputs:
            cost - a function that takes model parameters and data as inputs
                    and returns a single float
            data - the data the model is being fit to
            theta - a set model parameters
            ck - the step size to be used during perturbation of the model parameters

            Outputs:
            An estimate of the gradient
        """
        #Draw the perturbation

        delta=2.*scipy.stats.bernoulli.rvs(p=.5,size=theta.shape[0])-1.
        #hold delta constant for the parameters not under consideration
        delta[~param_ind]=0.
        #Perturb the parameters forwards and backwards
        thetaplus=theta+ck*delta
        thetaminus=theta-ck*delta

        #Evaluate the objective after the perturbations
        yplus=self.cost.evaluate(thetaplus)
        yminus=self.cost.evaluate(thetaminus)

        #Compute the slope across the perturbation

        ghat=(yplus-yminus)/(2*ck*delta)

        ghat[~param_ind]=0
        return ghat