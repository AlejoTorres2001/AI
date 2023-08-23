import api from "../api/client";
import { Parameters } from "../models/parameters";
import SummaryAxiosResponse from "../models/summary-response";

export async function summarize(file: File, parameters: Parameters) {
  try {
    const formData = new FormData();
    formData.append("file", file);
    formData.append("parameters", JSON.stringify(parameters));
    const response = await api.post<SummaryAxiosResponse>(
      "/summarize",
      formData
    );
    const data = response.data;
    return {
      summary: data.summary,
      message: data.message,
      ok: true,
    };
  } catch (error: any) {
    console.log("Este es el error", error);
    return {
      ok: false,
      message: error.response.data.message,
      summary: "",
    };
  }
}
