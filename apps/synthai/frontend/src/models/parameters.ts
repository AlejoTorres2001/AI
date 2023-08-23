export interface Parameters {
  language: "EN" | "ES";
  max_sequence_length: number;
  temperature: number;
  top_k: number;
  top_p: number;
}
export const defaultParameters: Parameters = {
  language: "EN",
  max_sequence_length: 2048,
  temperature: 0,
  top_k: 0.1,
  top_p: 0.1,
}