export interface INNParams {
  layer_params: ILayerParams[];
}

export interface ILayerParams {
  filter_size: number | string;
  num_filters: number | string;
}
