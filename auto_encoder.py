import pandas as pd
from keras import Sequential
from keras.layers import Dense
from utils_kdd99 import load_data, attack_label_class, correspondences, train_test_split, RANDOM_SEED
import numpy as np
def main():
    # input train and test data
    X, y = load_data(use_full_dataset=False, standard_scale=True, verbose=0, )
    # convert X labels to numbers
    y = y.map(lambda x: attack_label_class[x]).map(lambda x: correspondences[x])
    x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=RANDOM_SEED, stratify=y)
    model = Sequential([
        Dense(units=10, activation='relu', input_dim=38, name='encoder1'),
        Dense(units=5, activation='relu', name='encoder2'),
        Dense(units=10, activation='relu'),
        Dense(units=38, activation='relu'),
    ])
    model.compile(optimizer='adam', loss='mean_squared_error')
    model.fit(x=x_train, y=x_train, epochs=5, batch_size=32, shuffle=True, validation_split=0.20)
    encoders = Sequential([
        model.get_layer('encoder1'),
        model.get_layer('encoder2')
    ])
    columns = list(map(lambda x: 'feature' + str(x), range(5)))
    x_train_encoded = pd.DataFrame(data=encoders.predict(x_train), index=x_train.index, columns=columns)
    x_test_encoded = pd.DataFrame(data=encoders.predict(x_test), index=x_test.index, columns=columns)
    x_train_new_feature = x_train.merge(x_train_encoded, right_index=True, left_index=True)
    x_test_new_feature = x_test.merge(x_test_encoded, right_index=True, left_index=True)
    x_train_encoded.to_pickle("models/kdd99_features/x_train_encoded_5_df&activation=relu&epochs=5&batch_size=32.pkl")
    x_test_encoded.to_pickle("models/kdd99_features/x_test_encoded_5_df&activation=relu&epochs=5&batch_size=32.pkl")
    x_train_new_feature.to_pickle("models/kdd99_features/x_train+ae_43_df&activation=relu&epochs=5&batch_size=32"
                                  ".pkl")
    x_test_new_feature.to_pickle("models/kdd99_features/x_test+ae_43_df&activation=relu&epochs=5&batch_size=32.pkl")
    y_train.to_pickle("models/kdd99_features/y_train_df.pkl")
    y_test.to_pickle("models/kdd99_features/y_test_df.pkl")


if __name__ == '__main__':
    main()