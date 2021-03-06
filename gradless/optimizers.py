# AUTOGENERATED! DO NOT EDIT! File to edit: 01_optimizers.ipynb (unless otherwise specified).

__all__ = ['GradientDescent']

# Cell
import numpy
import scipy
from .gradient import SPSAGradient


# Cell
class GradientDescent():
    def __init__(self,x_0, model, update, gradient=None, acceptance_rule=None,
                 param_stepsize=1, param_stepdecay=.4, param_decay_offset=0,
                 grad_stepsize=1, grad_stepdecay=.2,
                seed=None):
        if seed is not None:
            assert type(seed) is int
            numpy.random.seed(seed)
        # store the model
        self.cost=model

        # Call the model once to ensure evaluate returns a float

#         test_val=self.cost.evaluate(x_0)
#         print (isinstance(test_val,float))
        try:
            numpy.isnan(self.cost.evaluate(x_0))
        except: raise(AssertionError("The cost function must return a float or an array with shape (1,) (e.g. not an array)"))
#         assert isinstance(test_val,float) or test_val.shape==(1), "The cost function must return a float or an array with shape (1,) (e.g. not an array)"

        self.update=update
        if gradient is None: gradient=SPSAGradient()
        self.gradient=gradient

        #if the gradient was passed without cost being defined, set the cost
        if self.gradient.cost is None:
            self.gradient.set_cost(self.cost)

        self.param_stepsize=param_stepsize
        self.param_stepdecay=param_stepdecay
        self.param_decay_offset=param_decay_offset
        self.grad_stepsize=grad_stepsize
        self.grad_stepdecay=grad_stepdecay
        self.t=0.
        self.cost_history=[self.cost.evaluate(x_0)]

        self.theta_hist=[x_0]
        self.theta=x_0

        self.acceptance_rule=acceptance_rule
        if self.acceptance_rule is not None:
            self.acceptance_rule.initialize(self)

    def update_params (self, gradient_reps=1,block_val=None, update_rvs=False):
        """This performs a single update of the model parameters"""
        self.t+=1

        c_k=self.grad_step()
        ### get the gradient
        ghat= self.gradient.evaluate( self.theta, c_k, gradient_reps=gradient_reps, update_rvs=update_rvs )


        ### determine the proposed step
        a_k=self.param_step()
        step=self.update.evaluate(ghat, a_k ,self.t)



        ### update the parameters
        new_theta=self.theta-step
        new_cost=self.cost.evaluate(new_theta)

        #I want to replace this with an acceptance rule

        #Always reject nans
        if numpy.isnan(new_cost):
            self.t-=1
            return()

        #Evaluate the acceptance criterion here
        if self.acceptance_rule is not None:
            accept=self.acceptance_rule.evaluate(new_cost, self.t)
            if accept==False:
                self.t-=1
                return()

        if block_val is not None:
            if self.t<100:
                if new_cost>(1.5*self.cost_history[-1]):
                    self.t-=1
                    return()
            else:
#                 mean_cost=numpy.mean(self.cost_history[-100:])
                sd_cost=numpy.std(self.cost_history[-100:])
                if new_cost>(block_val*sd_cost+self.cost_history[-1]):
                    self.t-=1
                    return()

        ### evaluate the objective function

        self.theta_hist.append(new_theta)
        self.theta=new_theta

        self.cost_history.append(new_cost)

    def fit(self, niter=10000, init_grad_reps=100):
        """This performs a set number of gradient descent descent iterations, along with some initialization"""
        pass
    def param_step(self):
        """This determines the step size used to update the model parameters.

        a_k= a/(t+A)**alpha"""
        return  (self.param_stepsize / (self.t+self.param_decay_offset)**self.param_stepdecay)

    def grad_step(self):
        """This determines the step size used to perturb the parameters during the gradient approximation"""
        return (self.grad_stepsize/(self.t)**self.grad_stepdecay)
