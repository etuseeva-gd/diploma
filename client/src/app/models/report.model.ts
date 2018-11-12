export interface IReport {
  is_train_ended: boolean;
  statistics: IStatisticPerEpoch[];
}

export interface IStatisticPerEpoch {
  epoch: number;

  train_accuracy: number;
  train_loss: number;

  test_accuracy: number;
  test_loss: number;
}
