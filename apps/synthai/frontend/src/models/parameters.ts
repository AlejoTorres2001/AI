export interface Parameters {
  language: "EN" | "SP";
  max_sequence_length: number;
  temperature: number;
  top_k: number;
  top_p: number;
  clusters_number: number;
  chunk_size: number;
  chunk_overlap: number;
}
export const defaultParameters: Parameters = {
  language: "EN",
  max_sequence_length: 2048,
  temperature: 0,
  top_k: 0.1,
  top_p: 0.1,
  clusters_number: 5,
  chunk_size: 500,
  chunk_overlap: 50,
};
