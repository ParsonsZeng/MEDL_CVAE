import tensorflow as tf
import tensorflow.contrib.slim as slim

FLAGS = tf.app.flags.FLAGS

class vae:

	def __init__(self,is_training):

		z_dim = FLAGS.z_dim

		self.input_image = tf.placeholder(dtype=tf.float32,shape=[None,3,128],name='input_image')
		
		self.input_nlcd = tf.placeholder(dtype=tf.float32,shape=[None,15],name='input_nlcd')
		
		self.input_label = tf.placeholder(dtype=tf.float32,shape=[None,100],name='input_label')

		self.keep_prob = tf.placeholder(tf.float32)

		weights_regularizer=slim.l2_regularizer(FLAGS.weight_decay)


		############## image feature ########
		# batch_norm = slim.batch_norm
		# batch_norm_params = {'is_training':is_training,'updates_collections':tf.GraphKeys.UPDATE_OPS,'decay':0.9,'epsilon':0.00001}

		#Padding: conv2d default is 'SAME'
		#Padding: pool2d default is 'VALID'
		
		# x = tf.expand_dims(self.input_image,-1)

		# x = slim.conv2d(scope='encoder/conv1',inputs=x,num_outputs=16,kernel_size=[3,3],stride=[3,1],
		# 	normalizer_fn=slim.batch_norm,normalizer_params=batch_norm_params,weights_regularizer = weights_regularizer)

		# x = slim.max_pool2d(scope='encoder/pool1',inputs=x,kernel_size=[3,2],stride=[3,2],padding='SAME')

		# x = slim.conv2d(scope='encoder/conv2',inputs=x,num_outputs=32,kernel_size=[1,3],stride=[1,1],
		# 	normalizer_fn=slim.batch_norm,normalizer_params=batch_norm_params,weights_regularizer = weights_regularizer)		

		# x = slim.max_pool2d(scope='encoder/pool2',inputs=x,kernel_size=[1,2],stride=[1,2],padding='SAME')

		# x = slim.conv2d(scope='encoder/conv3',inputs=x,num_outputs=64,kernel_size=[1,3],stride=[1,1],
		# 	normalizer_fn=slim.batch_norm,normalizer_params=batch_norm_params,weights_regularizer = weights_regularizer)

		# x = slim.max_pool2d(scope='encoder/pool3',inputs=x,kernel_size=[1,2],stride=[1,2],padding='SAME')

		# x = slim.conv2d(scope='encoder/conv4',inputs=x,num_outputs=128,kernel_size=[1,3],stride=[1,1],
		# 	normalizer_fn=slim.batch_norm,normalizer_params=batch_norm_params,weights_regularizer = weights_regularizer)

		# x = slim.max_pool2d(scope='encoder/pool4',inputs=x,kernel_size=[1,2],stride=[1,2],padding='SAME')

		# x = slim.conv2d(scope='encoder/conv5',inputs=x,num_outputs=256,kernel_size=[1,3],stride=[1,1],
		# 	normalizer_fn=slim.batch_norm,normalizer_params=batch_norm_params,weights_regularizer = weights_regularizer)

		# x = slim.max_pool2d(scope='encoder/pool5',inputs=x,kernel_size=[1,2],stride=[1,2],padding='SAME')

		# x = slim.conv2d(scope='encoder/conv6',inputs=x,num_outputs=512,kernel_size=[1,3],stride=[1,1],
		# 	normalizer_fn=slim.batch_norm,normalizer_params=batch_norm_params,weights_regularizer = weights_regularizer)

		# x = slim.max_pool2d(scope='encoder/pool6',inputs=x,kernel_size=[1,2],stride=[1,2],padding='SAME')

		# x = tf.reshape(x,[-1,512])

		# x = slim.fully_connected(x, 256,weights_regularizer=weights_regularizer, scope='encoder/hist/fc_1')
		# self.image_feature_encoder = slim.fully_connected(x, 100,weights_regularizer=weights_regularizer, scope='encoder/hist/fc_2')

		

		flatten_hist = tf.reshape(self.input_image,[-1,3*128])
		# x = slim.fully_connected(flatten_hist, 256,weights_regularizer=weights_regularizer,scope='encoder/hist/fc_1')
		# x = slim.fully_connected(x, 256,weights_regularizer=weights_regularizer, scope='encoder/hist/fc_2')
		# x = slim.fully_connected(x, 100,weights_regularizer=weights_regularizer, scope='encoder/hist/fc_3')
		# self.image_feature_encoder = x
		self.image_feature_encoder = flatten_hist
		

		#self.image_feature_encoder = slim.dropout(x,keep_prob=self.keep_prob,is_training=is_training)

		############## Q(z|X) ###############

		input_x = tf.concat([self.input_nlcd,self.image_feature_encoder,self.input_label],1)

		#input_x = tf.concat([self.input_nlcd,self.input_label],1)

		#input_x = slim.dropout(input_x,keep_prob=self.keep_prob,is_training=is_training)

		x = slim.fully_connected(input_x, 512,weights_regularizer=weights_regularizer,scope='encoder/fc_1')
		x = slim.fully_connected(x, 1024,weights_regularizer=weights_regularizer, scope='encoder/fc_2')
		x = slim.fully_connected(x, 499,weights_regularizer=weights_regularizer, scope='encoder/fc_3')

		#x = x+input_x

		#dropout
		#x = slim.dropout(x,keep_prob=self.keep_prob,is_training=is_training)

		z_miu = slim.fully_connected(x, z_dim, activation_fn=None, weights_regularizer=weights_regularizer,scope='encoder/z_miu')
		z_logvar = slim.fully_connected(x, z_dim, activation_fn=None, weights_regularizer=weights_regularizer,scope='encoder/z_logvar')

		############## Sample_z ###############

		eps = tf.random_normal(shape=tf.shape(z_miu))
		sample_z = z_miu + tf.exp(z_logvar / 2) * eps

		############## P(X|z) ###############

		flatten_hist = tf.reshape(self.input_image,[-1,3*128])
		# x = slim.fully_connected(flatten_hist, 256,weights_regularizer=weights_regularizer,scope='decoder/hist/fc_1')
		# x = slim.fully_connected(x, 256,weights_regularizer=weights_regularizer, scope='decoder/hist/fc_2')
		# x = slim.fully_connected(x, 100,weights_regularizer=weights_regularizer, scope='decoder/hist/fc_3')

		# self.image_feature_decoder = slim.dropout(x,keep_prob=self.keep_prob,is_training=is_training)

		# x = tf.expand_dims(self.input_image,-1)

		# x = slim.conv2d(scope='decoder/conv1',inputs=x,num_outputs=16,kernel_size=[3,3],stride=[3,1],
		# 	normalizer_fn=slim.batch_norm,normalizer_params=batch_norm_params,weights_regularizer = weights_regularizer)

		# x = slim.max_pool2d(scope='decoder/pool1',inputs=x,kernel_size=[3,2],stride=[3,2],padding='SAME')

		# x = slim.conv2d(scope='decoder/conv2',inputs=x,num_outputs=32,kernel_size=[1,3],stride=[1,1],
		# 	normalizer_fn=slim.batch_norm,normalizer_params=batch_norm_params,weights_regularizer = weights_regularizer)		

		# x = slim.max_pool2d(scope='decoder/pool2',inputs=x,kernel_size=[1,2],stride=[1,2],padding='SAME')

		# x = slim.conv2d(scope='decoder/conv3',inputs=x,num_outputs=64,kernel_size=[1,3],stride=[1,1],
		# 	normalizer_fn=slim.batch_norm,normalizer_params=batch_norm_params,weights_regularizer = weights_regularizer)

		# x = slim.max_pool2d(scope='decoder/pool3',inputs=x,kernel_size=[1,2],stride=[1,2],padding='SAME')

		# x = slim.conv2d(scope='decoder/conv4',inputs=x,num_outputs=128,kernel_size=[1,3],stride=[1,1],
		# 	normalizer_fn=slim.batch_norm,normalizer_params=batch_norm_params,weights_regularizer = weights_regularizer)

		# x = slim.max_pool2d(scope='decoder/pool4',inputs=x,kernel_size=[1,2],stride=[1,2],padding='SAME')

		# x = slim.conv2d(scope='decoder/conv5',inputs=x,num_outputs=256,kernel_size=[1,3],stride=[1,1],
		# 	normalizer_fn=slim.batch_norm,normalizer_params=batch_norm_params,weights_regularizer = weights_regularizer)

		# x = slim.max_pool2d(scope='decoder/pool5',inputs=x,kernel_size=[1,2],stride=[1,2],padding='SAME')

		# x = slim.conv2d(scope='decoder/conv6',inputs=x,num_outputs=512,kernel_size=[1,3],stride=[1,1],
		# 	normalizer_fn=slim.batch_norm,normalizer_params=batch_norm_params,weights_regularizer = weights_regularizer)

		# x = slim.max_pool2d(scope='decoder/pool6',inputs=x,kernel_size=[1,2],stride=[1,2],padding='SAME')

		# x = tf.reshape(x,[-1,512])

		# x = slim.fully_connected(x, 256,weights_regularizer=weights_regularizer, scope='decoder/hist/fc_1')
		# self.image_feature_decoder = slim.fully_connected(x, 100,weights_regularizer=weights_regularizer, scope='decoder/hist/fc_2')


		self.image_feature_decoder = flatten_hist
		input_x = tf.concat([self.input_nlcd,self.image_feature_decoder,sample_z],1)
		#x = tf.concat([self.input_nlcd,sample_z],1)

		x = slim.fully_connected(input_x, 512,weights_regularizer=weights_regularizer,scope='decoder/fc_1')
		x = slim.fully_connected(x, 1024,weights_regularizer=weights_regularizer, scope='decoder/fc_2')
		x = slim.fully_connected(x, 499,weights_regularizer=weights_regularizer, scope='decoder/fc_3')

		#x = x+input_x
		
		#dropout
		x = slim.dropout(x,keep_prob=self.keep_prob,is_training=is_training)
		
		self.logits = slim.fully_connected(x, 100, activation_fn=None, weights_regularizer=weights_regularizer,scope='decoder/logits')

		self.output = tf.sigmoid(self.logits,name='decoder/output')

		# E[log P(X|z)]
		self.recon_loss = tf.reduce_mean(tf.reduce_sum(tf.nn.sigmoid_cross_entropy_with_logits(logits=self.logits, labels=self.input_label), 1))
		tf.summary.scalar('recon_loss',self.recon_loss)
		
		# D_KL(Q(z|X) || P(z|X)); calculate in closed form as both dist. are Gaussian
		self.kl_loss = tf.reduce_mean(0.5 * tf.reduce_sum(tf.exp(z_logvar) + z_miu**2 - 1. - z_logvar, 1))
		tf.summary.scalar('kl_loss',self.kl_loss)

		# VAE loss
		self.vae_loss = self.recon_loss + self.kl_loss
		slim.losses.add_loss(self.vae_loss)
		tf.summary.scalar('vae_loss',self.vae_loss)
		
		# l2 loss
		self.l2_loss = tf.add_n(slim.losses.get_regularization_losses())
		tf.summary.scalar('l2_loss',self.l2_loss)

		#total loss
		self.total_loss = slim.losses.get_total_loss()
		tf.summary.scalar('total_loss',self.total_loss)





		# self.g_output = tf.sigmoid(x)

		# self.ce_loss = tf.reduce_mean(tf.reduce_sum(tf.nn.sigmoid_cross_entropy_with_logits(labels=self.input_label,logits=x),1))

		# tf.summary.scalar('ce_loss',self.ce_loss)

		# slim.losses.add_loss(self.ce_loss)		

		# self.l2_loss = tf.add_n(slim.losses.get_regularization_losses())

		# tf.summary.scalar('l2_loss',self.l2_loss)

		# self.total_loss = slim.losses.get_total_loss()

		# tf.summary.scalar('total_loss',self.total_loss)

		# self.output = tf.sigmoid(x)

		