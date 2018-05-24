import preprocessing

if __name__ == "__main__":
        preprocessing.make_training_set().to_csv("dataset.csv", sep='\t', encoding='utf-8', index=False)


