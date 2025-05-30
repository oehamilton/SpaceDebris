import numpy as np
X_test = np.load("SpaceDebris/data/preprocessed/X_test.npy")
y_test = np.load("SpaceDebris/data/preprocessed/y_test.npy")
print("Test image shape:", X_test.shape)  # Should be (1, 128, 128, 3)
print("Test label:", y_test)  # Should be [0]