import numpy as np

from layers import *
from layer_utils import *


class TwoLayerNet(object):
  """
  A two-layer fully-connected neural network with ReLU nonlinearity and
  softmax loss that uses a modular layer design. We assume an input dimension
  of d, a hidden dimension of h, and perform classification over C classes.
  
  The architecure should be affine - relu - affine - softmax.

  Note that this class does not implement gradient descent; instead, it
  will interact with a separate Solver object that is responsible for running
  optimization.

  The learnable parameters of the model are stored in the dictionary
  self.params that maps parameter names to numpy arrays.
  """
  
  def __init__(self, input_dim=3*32*32, hidden_dim=100, num_classes=10,
               weight_scale=1e-3, reg=0.0):
    """
    Initialize a new network.

    Inputs:
    - input_dim: An integer giving the size of the input
    - hidden_dim: An integer giving the size of the hidden layer
    - num_classes: An integer giving the number of classes to classify
    - dropout: Scalar between 0 and 1 giving dropout strength.
    - weight_scale: Scalar giving the standard deviation for random
      initialization of the weights.
    - reg: Scalar giving L2 regularization strength.
    """
    self.params = {}
    self.reg = reg
    
    ############################################################################
    # TODO: Initialize the weights and biases of the two-layer net. Weights    #
    # should be initialized from a Gaussian with standard deviation equal to   #
    # weight_scale, and biases should be initialized to zero. All weights and  #
    # biases should be stored in the dictionary self.params, with first layer  #
    # weights and biases using the keys 'theta1' and 'theta1_0' and second     #
    # layer weights and biases using the keys 'theta2' and 'theta2_0.          #
    ############################################################################
    # 4 lines of code expected
    self.params['theta1'] = np.random.normal(0.0, weight_scale, (input_dim, hidden_dim))
    self.params['theta1_0'] = np.zeros((1, hidden_dim))
    self.params['theta2'] = np.random.normal(0.0, weight_scale, (hidden_dim, num_classes))
    self.params['theta2_0'] = np.zeros((1, num_classes))
    pass
    ############################################################################
    #                             END OF YOUR CODE                             #
    ############################################################################


  def loss(self, X, y=None):
    """
    Compute loss and gradient for a minibatch of data.

    Inputs:
    - X: Array of input data of shape (m, d_1, ..., d_k)
    - y: Array of labels, of shape (m,). y[i] gives the label for X[i].

    Returns:
    If y is None, then run a test-time forward pass of the model and return:
    - scores: Array of shape (m, C) giving classification scores, where
      scores[i, c] is the classification score for X[i] and class c.

    If y is not None, then run a training-time forward and backward pass and
    return a tuple of:
    - loss: Scalar value giving the loss
    - grads: Dictionary with the same keys as self.params, mapping parameter
      names to gradients of the loss with respect to those parameters.
    """  
    scores = None
    ############################################################################
    # TODO: Implement the forward pass for the two-layer net, computing the    #
    # class scores for X and storing them in the scores variable.              #
    ############################################################################
    # Hint: unpack the weight parameters from self.params
    # 3 lines of code expected
    x1, cache_1 = affine_relu_forward(X, self.params['theta1'], self.params['theta1_0'])
    scores, cache_2 = affine_forward(x1, self.params['theta2'], self.params['theta2_0'])

    ############################################################################
    #                             END OF YOUR CODE                             #
    ############################################################################

    # If y is None then we are in test mode so just return scores
    if y is None:
      return scores
    
    loss, grads = 0, {}
    ############################################################################
    # TODO: Implement the backward pass for the two-layer net. Store the loss  #
    # in the loss variable and gradients in the grads dictionary. Compute data #
    # loss using softmax, and make sure that grads[k] holds the gradients for  #
    # self.params[k]. Don't forget to add L2 regularization!                   #
    #                                                                          #
    # NOTE: To ensure that your implementation matches ours and you pass the   #
    # automated tests, make sure that your L2 regularization includes a factor #
    # of 0.5 to simplify the expression for the gradient.                      #
    ############################################################################
    # 4-8 lines of code expected
    loss, grad = softmax_loss(scores, y)
    loss += 0.5 * self.reg * (self.params['theta1']**2).sum()+ 0.5 * self.reg * (self.params['theta2']**2).sum()
    grad_x2, grads['theta2'], grads['theta2_0'] = affine_backward(grad, cache_2)
    grads['theta2'] += self.reg * self.params['theta2'] 
    _, grads['theta1'], grads['theta1_0'] = affine_relu_backward(grad_x2, cache_1)
    grads['theta1'] += self.reg * self.params['theta1'] 
    ############################################################################
    #                             END OF YOUR CODE                             #
    ############################################################################

    return loss, grads


class FullyConnectedNet(object):
  """
  A fully-connected neural network with an arbitrary number of hidden layers,
  ReLU nonlinearities, and a softmax loss function. This will also implement
  dropout as an option. For a network with L layers,
  the architecture will be
  
  {affine - - relu - [dropout]} x (L - 1) - affine - softmax
  
  where  dropout is  optional, and the {...} block is
  repeated L - 1 times.
  
  Similar to the TwoLayerNet above, learnable parameters are stored in the
  self.params dictionary and will be learned using the Solver class.
  """

  def __init__(self, hidden_dims, input_dim=3*32*32, num_classes=10,
               dropout=0, reg=0.0,
               weight_scale=1e-2, dtype=np.float32, seed=None):
    """
    Initialize a new FullyConnectedNet.
    
    Inputs:
    - hidden_dims: A list of integers giving the size of each hidden layer.
    - input_dim: An integer giving the size of the input.
    - num_classes: An integer giving the number of classes to classify.
    - dropout: Scalar between 0 and 1 giving dropout strength. If dropout=0 then
      the network should not use dropout at all.
    - reg: Scalar giving L2 regularization strength.
    - weight_scale: Scalar giving the standard deviation for random
      initialization of the weights.
    - dtype: A numpy datatype object; all computations will be performed using
      this datatype. float32 is faster but less accurate, so you should use
      float64 for numeric gradient checking.
    - seed: If not None, then pass this random seed to the dropout layers. This
      will make the dropout layers deteriminstic so we can gradient check the
      model.
    """
    self.use_dropout = dropout > 0
    self.reg = reg
    self.num_layers = 2 + len(hidden_dims)
    self.dtype = dtype
    self.params = {}

    ############################################################################
    # TODO: Initialize the parameters of the network, storing all values in    #
    # the self.params dictionary. Store weights and biases for the first layer #
    # in theta1 and theta1_0 for the second layer use theta2 and theta2_0, etc.#
    # Weights should beinitialized from a normal distribution with standard    #
    # deviation equal to weight_scale and biases should be initialized to zero.#
    #                                                                          #
    ############################################################################
    # about 4 lines of code
    self.params['theta1'] = np.random.normal(0.0, weight_scale, (input_dim, hidden_dims[0]))
    self.params['theta1_0'] = np.zeros((1, hidden_dims[0]))
    for hiddenCount in range(len(hidden_dims) - 1):
        thetaName = 'theta' + str(hiddenCount + 2)
        theta0Name = thetaName + '_0'
        self.params[thetaName] = np.random.normal(0.0, weight_scale, (hidden_dims[hiddenCount], hidden_dims[hiddenCount + 1]))
        self.params[theta0Name] = np.zeros((1, hidden_dims[hiddenCount + 1]))
    self.params['theta' + str(len(hidden_dims) + 1)] = np.random.normal(0.0, weight_scale, (hidden_dims[-1], num_classes))
    self.params['theta' + str(len(hidden_dims) + 1) + '_0'] = np.zeros((1, num_classes))
    ############################################################################
    #                             END OF YOUR CODE                             #
    ############################################################################

    # When using dropout we need to pass a dropout_param dictionary to each
    # dropout layer so that the layer knows the dropout probability and the mode
    # (train / test). You can pass the same dropout_param to each dropout layer.

    self.dropout_param = {}
    if self.use_dropout:
      self.dropout_param = {'mode': 'train', 'p': dropout}
      if seed is not None:
        self.dropout_param['seed'] = seed
    
    # Cast all parameters to the correct datatype

    for k, v in self.params.iteritems():
      self.params[k] = v.astype(dtype)


  def loss(self, X, y=None):
    """
    Compute loss and gradient for the fully-connected net.

    Input / output: Same as TwoLayerNet above.
    """
    X = X.astype(self.dtype)
    mode = 'test' if y is None else 'train'

    # Set train/test mode for  dropout param since they
    # behave differently during training and testing.
    if self.dropout_param is not None:
      self.dropout_param['mode'] = mode   

    scores = None
    ############################################################################
    # TODO: Implement the forward pass for the fully-connected net, computing  #
    # the class scores for X and storing them in the scores variable.          #
    #                                                                          #
    # When using dropout, you'll need to pass self.dropout_param to each       #
    # dropout forward pass.                                                    #
    #                                                                          #
    ############################################################################
    xRepository = {}
    cacheRepository = {}
    dropoutRepository = {}
    
    if self.use_dropout:
        xRepository['x1'], cacheRepository['cache1'] = affine_relu_forward(X, self.params['theta1'], self.params['theta1_0'])
        xRepository['x1'], dropoutRepository['cache1'] = dropout_forward(xRepository['x1'], self.dropout_param)
    else:
        xRepository['x1'], cacheRepository['cache1'] = affine_relu_forward(X, self.params['theta1'], self.params['theta1_0'])
        
    for hiddenCount in range(self.num_layers - 3):
        xName = 'x' + str(hiddenCount + 2)
        xNamePre = 'x' + str(hiddenCount + 1)
        cacheName = 'cache' + str(hiddenCount + 2)
        if self.use_dropout:
            xRepository[xName], cacheRepository[cacheName] = affine_relu_forward(xRepository[xNamePre], 
                                                         self.params['theta'+str(hiddenCount + 2)], self.params['theta'+str(hiddenCount + 2)+'_0'])
            xRepository[xName], dropoutRepository[cacheName] = dropout_forward(xRepository[xName], self.dropout_param)   
        else:
            xRepository[xName], cacheRepository[cacheName] = affine_relu_forward(xRepository[xNamePre], 
                                                         self.params['theta'+str(hiddenCount + 2)], self.params['theta'+str(hiddenCount + 2)+'_0'])                              
    
    scores, cacheOutput = affine_forward(xRepository['x' + str(self.num_layers - 2)], 
                                 self.params['theta' + str(self.num_layers - 1)], self.params['theta' + str(self.num_layers - 1)+'_0'])
    
    ############################################################################
    #                             END OF YOUR CODE                             #
    ############################################################################

    # If test mode return early
    if mode == 'test':
      return scores

    loss, grads = 0.0, {}
    ############################################################################
    # TODO: Implement the backward pass for the fully-connected net. Store the #
    # loss in the loss variable and gradients in the grads dictionary. Compute #
    # data loss using softmax, and make sure that grads[k] holds the gradients #
    # for self.params[k]. Don't forget to add L2 regularization!               #
    #                                                                          #
    #                                                                          #
    # NOTE: To ensure that your implementation matches ours and you pass the   #
    # automated tests, make sure that your L2 regularization includes a factor #
    # of 0.5 to simplify the expression for the gradient.                      #
    ############################################################################
    loss, gradOutput = softmax_loss(scores, y)
    gradRepository = {}
    
    for i in range(self.num_layers - 1):
        loss += 0.5 * self.reg * (self.params['theta' + str(i + 1)] ** 2).sum()
        
    if self.use_dropout: 
        gradRepository['x' + str(self.num_layers -2)], grads['theta' + str(self.num_layers - 1)], \
                       grads['theta' + str(self.num_layers - 1) + '_0'] = affine_backward(gradOutput, cacheOutput)
        gradRepository['x' + str(self.num_layers -2)] = dropout_backward(gradRepository['x' + str(self.num_layers -2)], dropoutRepository['cache' + str(self.num_layers -2)])                
    else:
        gradRepository['x' + str(self.num_layers -2)], grads['theta' + str(self.num_layers - 1)], \
                       grads['theta' + str(self.num_layers - 1) + '_0'] = affine_backward(gradOutput, cacheOutput)
    grads['theta' + str(self.num_layers - 1)] += self.reg * self.params['theta' + str(self.num_layers - 1)] 
    
    for hiddenCount in reversed(range(1, self.num_layers - 1)):
        if self.use_dropout: 
            gradRepository['x' + str(hiddenCount - 1)], grads['theta'+str(hiddenCount)], grads['theta'+str(hiddenCount) + '_0'] =  \
                                             affine_relu_backward(gradRepository['x' + str(hiddenCount)], cacheRepository['cache' + str(hiddenCount)])
            if hiddenCount > 1:
                gradRepository['x' + str(hiddenCount - 1)] = dropout_backward(gradRepository['x' + str(hiddenCount - 1)], dropoutRepository['cache' + str(hiddenCount - 1)])                                 
        else:
            gradRepository['x' + str(hiddenCount - 1)], grads['theta'+str(hiddenCount)], grads['theta'+str(hiddenCount) + '_0'] =  \
                                             affine_relu_backward(gradRepository['x' + str(hiddenCount)], cacheRepository['cache' + str(hiddenCount)])
        grads['theta'+str(hiddenCount)] += self.reg * self.params['theta'+str(hiddenCount)] 
    ############################################################################
    #                             END OF YOUR CODE                             #
    ############################################################################

    return loss, grads
