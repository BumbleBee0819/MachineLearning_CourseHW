import numpy as np


def affine_forward(x, theta, theta0):
  """
  Computes the forward pass for an affine (fully-connected) layer.

  The input x has shape (m, d_1, ..., d_k) and contains a minibatch of m
  examples, where each example x[i] has shape (d_1, ..., d_k). We will
  reshape each input into a vector of dimension d = d_1 * ... * d_k, and
  then transform it to an output vector of dimension h.

  Inputs:
  - x: A numpy array containing input data, of shape (m, d_1, ..., d_k)
  - theta: A numpy array of weights, of shape (d, h)
  - theta0: A numpy array of biases, of shape (h,)
  
  Returns a tuple of:
  - out: output, of shape (m, h)
  - cache: (x, theta, theta0)
  """
  out = None
  #############################################################################
  # TODO: Implement the affine forward pass. Store the result in out. You     #
  # will need to reshape the input into rows.                                 #
  #############################################################################
  # 2 lines of code expected
  X = x.reshape((x.shape[0],-1))
  out = X.dot(theta) + theta0
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################
  cache = (x, theta, theta0)
  return out, cache


def affine_backward(dout, cache):
  """
  Computes the backward pass for an affine layer.

  Inputs:
  - dout: Upstream derivative, of shape (m, h)
  - cache: Tuple of:
    - x: Input data, of shape (m, d_1, ... d_k)
    - theta: Weights, of shape (d,h)
    - theta0: biases, of shape (h,)

  Returns a tuple of:
  - dx: Gradient with respect to x, of shape (m, d1, ..., d_k)
  - dtheta: Gradient with respect to theta, of shape (d, h)
  - dtheta0: Gradient with respect to theta0, of shape (1,h)
  """
  x, theta, theta0 = cache
  dx, dtheta, dtheta0 = None, None, None
  #############################################################################
  # TODO: Implement the affine backward pass.                                 #
  #############################################################################
  # Hint: do not forget to reshape x into (m,d) form
  # 4-5 lines of code expected
  dim = x.shape
  X = x.reshape((x.shape[0],-1))
  dx = dout.dot(theta.T).reshape(dim)
  dtheta = (X.T).dot(dout) 
  dtheta0 = np.ones([1, dim[0]]).dot(dout) 
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################
  return dx, dtheta, dtheta0


def relu_forward(x):
  """
  Computes the forward pass for a layer of rectified linear units (ReLUs).

  Input:
  - x: Inputs, of any shape

  Returns a tuple of:
  - out: Output, of the same shape as x
  - cache: x
  """
  out = None
  #############################################################################
  # TODO: Implement the ReLU forward pass.                                    #
  #############################################################################
  # 1 line of code expected
  out = np.maximum(x, 0)
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################
  cache = x
  return out, cache


def relu_backward(dout, cache):
  """
  Computes the backward pass for a layer of rectified linear units (ReLUs).

  Input:
  - dout: Upstream derivatives, of any shape
  - cache: Input x, of same shape as dout

  Returns:
  - dx: Gradient with respect to x
  """
  dx, x = None, cache
  #############################################################################
  # TODO: Implement the ReLU backward pass.                                   #
  #############################################################################
  # 1 line of code expected. Hint: use np.where
  dx = dout * np.where(x > 0, 1, 0)
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################
  return dx


def dropout_forward(x, dropout_param):
  """
  Performs the forward pass for (inverted) dropout.

  Inputs:
  - x: Input data, of any shape
  - dropout_param: A dictionary with the following keys:
    - p: Dropout parameter. We drop each neuron output with probability p.
    - mode: 'test' or 'train'. If the mode is train, then perform dropout;
      if the mode is test, then just return the input.
    - seed: Seed for the random number generator. Passing seed makes this
      function deterministic, which is needed for gradient checking but not in
      real networks.

  Outputs:
  - out: Array of the same shape as x.
  - cache: A tuple (dropout_param, mask). In training mode, mask is the dropout
    mask that was used to multiply the input; in test mode, mask is None.
  """
  p, mode = dropout_param['p'], dropout_param['mode']
  if 'seed' in dropout_param:
    np.random.seed(dropout_param['seed'])

  mask = None
  out = None

  if mode == 'train':
    ###########################################################################
    # TODO: Implement the training phase forward pass for inverted dropout.   #
    # Store the dropout mask in the mask variable.                            #
    ###########################################################################
    # 2 lines of code expected
    mask = (np.random.rand(*x.shape) < (1 - p)) / (1 - p)
    out = x * mask
    ###########################################################################
    #                            END OF YOUR CODE                             #
    ###########################################################################
  elif mode == 'test':
    ###########################################################################
    # TODO: Implement the test phase forward pass for inverted dropout.       #
    ###########################################################################
    # 1 line of code expected
    out = x 
    ###########################################################################
    #                            END OF YOUR CODE                             #
    ###########################################################################

  cache = (dropout_param, mask)
  out = out.astype(x.dtype, copy=False)

  return out, cache


def dropout_backward(dout, cache):
  """
  Perform the backward pass for (inverted) dropout.

  Inputs:
  - dout: Upstream derivatives, of any shape
  - cache: (dropout_param, mask) from dropout_forward.
  """
  dropout_param, mask = cache
  mode = dropout_param['mode']
  
  dx = None
  if mode == 'train':
    ###########################################################################
    # TODO: Implement the training phase backward pass for inverted dropout.  #
    ###########################################################################
    # 1 line of code expected
    dx = dout * mask 
    ###########################################################################
    #                            END OF YOUR CODE                             #
    ###########################################################################
  elif mode == 'test':
    dx = dout
  return dx


def conv_forward_naive(x, theta, theta0, conv_param):
  """
  A naive implementation of the forward pass for a convolutional layer.

  The input consists of m data points, each with C channels, height H and width
  W. We convolve each input with F different filters, where each filter spans
  all C channels and has height HH and width HH.

  Input:
  - x: Input data of shape (m, C, H, W)
  - theta: Filter weights of shape (F, C, HH, WW)
  - theta0: Biases, of shape (F,)
  - conv_param: A dictionary with the following keys:
    - 'stride': The number of pixels between adjacent receptive fields in the
      horizontal and vertical directions.
    - 'pad': The number of pixels that will be used to zero-pad the input.

  Returns a tuple of:
  - out: Output data, of shape (m, F, H', W') where H' and W' are given by
    H' = 1 + (H + 2 * pad - HH) / stride
    W' = 1 + (W + 2 * pad - WW) / stride
  - cache: (x, theta, theta0, conv_param)
  """
  out = None
  #############################################################################
  # TODO: Implement the convolutional forward pass.                           #
  # Hint: you can use the function np.pad for padding.                        #
  #############################################################################
  m, C, H, W = x.shape
  F, _, HH, WW = theta.shape
  stride, pad = conv_param['stride'], conv_param['pad']
  X = np.pad(x, ((0, 0), (0, 0), (pad, pad), (pad, pad)), mode='constant', constant_values=0)

  # Check dimensions
  assert (W + 2 * pad - WW) % stride == 0, 'width does not work'
  assert (H + 2 * pad - HH) % stride == 0, 'height does not work'

  # Create output
  H_prime = (H + 2 * pad - HH) / stride + 1
  W_prime = (W + 2 * pad - WW) / stride + 1
  out = np.zeros((m, F, H_prime, W_prime), dtype=x.dtype)
  
  #implement the convolution
  for sample in xrange(m):
      for filter in xrange(F):
          for i in xrange(H_prime):
              for j in xrange(W_prime):
                  out[sample, filter, i, j] = (X[sample, :, (i*stride) :((i*stride) + \
                      HH), (j*stride):((j*stride) + WW)] * theta[filter]).sum() + theta0[filter]
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################
  cache = (x, theta, theta0, conv_param)
  return out, cache


def conv_backward_naive(dout, cache):
  """
  A naive implementation of the backward pass for a convolutional layer.

  Inputs:
  - dout: Upstream derivatives.
  - cache: A tuple of (x, theta, theta0, conv_param) as in conv_forward_naive

  Returns a tuple of:
  - dx: Gradient with respect to x
  - dtheta: Gradient with respect to theta
  - dtheta0: Gradient with respect to theta0
  """
  dx, dtheta, dtheta0 = None, None, None
  #############################################################################
  # TODO: Implement the convolutional backward pass.                          #
  #############################################################################
  x, theta, theta0, conv_param = cache
  m, C, H, W = x.shape
  F, _, HH, WW = theta.shape
  _, _, H_prime, W_prime = dout.shape
  stride, pad = conv_param['stride'], conv_param['pad']
  
  dx = np.zeros_like(x)
  dtheta = np.zeros_like(theta)
  dtheta0 = np.zeros_like(theta0)
  
  dX = np.pad(dx, ((0, 0), (0, 0), (pad, pad), (pad, pad)), mode='constant', constant_values=0)
  X = np.pad(x, ((0, 0), (0, 0), (pad, pad), (pad, pad)), mode='constant', constant_values=0)
  
  for sample in xrange(m):
      for filter in xrange(F):
          for i in xrange(H_prime):
              for j in xrange(W_prime):
                  h0 = i * stride
                  h1 = i * stride + HH
                  w0 = j * stride
                  w1 = j * stride + WW
                  dtheta[filter] += dout[sample, filter, i, j] * X[sample, :, h0:h1, w0:w1]
                  dtheta0[filter] += dout[sample, filter, i, j]
                  dX[sample, :, h0:h1, w0:w1] += dout[sample, filter, i, j] * theta[filter]
                      
  dx = dX[:, :, pad:-pad, pad:-pad]              
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################
  return dx, dtheta, dtheta0


def max_pool_forward_naive(x, pool_param):
  """
  A naive implementation of the forward pass for a max pooling layer.

  Inputs:
  - x: Input data, of shape (m, C, H, W)
  - pool_param: dictionary with the following keys:
    - 'pool_height': The height of each pooling region
    - 'pool_width': The width of each pooling region
    - 'stride': The distance between adjacent pooling regions

  Returns a tuple of:
  - out: Output data
  - cache: (x, pool_param)
  """
  out = None
  #############################################################################
  # TODO: Implement the max pooling forward pass                              #
  #############################################################################
  m, C, H, W = x.shape
  H_pool, W_pool, stride = pool_param['pool_height'], pool_param['pool_width'], pool_param['stride']
  
    # Check dimensions
  assert (W - W_pool) % stride == 0, 'width does not work'
  assert (H - H_pool) % stride == 0, 'height does not work'
  
  H_prime = (H - H_pool) / stride + 1
  W_prime = (W - W_pool) / stride + 1
  
  out = np.zeros((m, C, H_prime, W_prime), dtype=x.dtype)
  
  for sample in xrange(m):
      for color in xrange(C):
          for i in xrange(H_prime):
              for j in xrange(W_prime):
                  h0 = i * stride
                  h1 = i * stride + H_pool
                  w0 = j * stride
                  w1 = j * stride + W_pool
                  out[sample, color, i, j] = np.max(x[sample, color, h0:h1, w0:w1])
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################
  cache = (x, pool_param)
  return out, cache


def max_pool_backward_naive(dout, cache):
  """
  A naive implementation of the backward pass for a max pooling layer.

  Inputs:
  - dout: Upstream derivatives
  - cache: A tuple of (x, pool_param) as in the forward pass.

  Returns:
  - dx: Gradient with respect to x
  """
  dx = None
  #############################################################################
  # TODO: Implement the max pooling backward pass                             #
  #############################################################################
  x, pool_param = cache
  H_pool, W_pool, stride = pool_param['pool_height'], pool_param['pool_width'], pool_param['stride']
  m, C, H, W = x.shape
  _, _, H_prime, W_prime = dout.shape
  
  dx = np.zeros_like(x)
  for sample in xrange(m):
      for color in xrange(C):
          for i in xrange(H_prime):
              for j in xrange(W_prime):
                  h0 = i * stride
                  h1 = i * stride + H_pool
                  w0 = j * stride
                  w1 = j * stride + W_pool
                  temp = x[sample, color, h0:h1, w0:w1]
                  indexMax = np.where(temp == temp.max())
                  maskMatrix = np.zeros([H_pool, W_pool])
                  maskMatrix[indexMax] = 1
                  dx[sample, color, h0:h1, w0:w1] = dout[sample, color, i, j] * maskMatrix
                  
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################
  return dx



def svm_loss(x, y):
  """
  Computes the loss and gradient using for multiclass SVM classification.

  Inputs:
  - x: Input data, of shape (m, C) where x[i, j] is the score for the jth class
    for the ith input.
  - y: Vector of labels, of shape (m,) where y[i] is the label for x[i] and
    0 <= y[i] < C

  Returns a tuple of:
  - loss: Scalar giving the loss
  - dx: Gradient of the loss with respect to x
  """
  m = x.shape[0]
  correct_class_scores = x[np.arange(m), y]
  margins = np.maximum(0, x - correct_class_scores[:, np.newaxis] + 1.0)
  margins[np.arange(m), y] = 0
  loss = np.sum(margins) / m
  num_pos = np.sum(margins > 0, axis=1)
  dx = np.zeros_like(x)
  dx[margins > 0] = 1
  dx[np.arange(m), y] -= num_pos
  dx /= m
  return loss, dx


def softmax_loss(x, y):
  """
  Computes the loss and gradient for softmax classification.

  Inputs:
  - x: Input data, of shape (m, C) where x[i, j] is the score for the jth class
    for the ith input.
  - y: Vector of labels, of shape (m,) where y[i] is the label for x[i] and
    0 <= y[i] < C

  Returns a tuple of:
  - loss: Scalar giving the loss
  - dx: Gradient of the loss with respect to x
  """
  probs = np.exp(x - np.max(x, axis=1, keepdims=True))
  probs /= np.sum(probs, axis=1, keepdims=True)
  m = x.shape[0]
  loss = -np.sum(np.log(probs[np.arange(m), y])) / m
  dx = probs.copy()
  dx[np.arange(m), y] -= 1
  dx /= m
  return loss, dx
