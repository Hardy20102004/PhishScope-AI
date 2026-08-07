import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query"
import { apiClient } from "@/api/client"

export interface Finding {
  title: string
  description: string
  severity: "LOW" | "MEDIUM" | "HIGH" | "CRITICAL"
}

export interface Investigation {
  id: string
  target: string
  type: "URL" | "DOMAIN" | "WEBSITE" | "EMAIL" | "MESSAGING" | "QR" | "FILE" | "APK"
  status: "PENDING" | "PROCESSING" | "COMPLETED" | "FAILED"
  risk_score: number | null
  risk_level: string | null
  evidence: Record<string, any>
  findings: Finding[]
  error_message: string | null
  created_at: string
  completed_at: string | null
  user_id: string
}

export const useGetInvestigations = () => {
  return useQuery({
    queryKey: ["investigations"],
    queryFn: async () => {
      const { data } = await apiClient.get<{ data: Investigation[] }>("/investigations")
      return data.data
    },
  })
}

export const useGetInvestigation = (id: string) => {
  return useQuery({
    queryKey: ["investigations", id],
    queryFn: async () => {
      const { data } = await apiClient.get<{ data: Investigation }>(`/investigations/${id}`)
      return data.data
    },
    enabled: !!id,
  })
}

export const useSubmitInvestigation = () => {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: async (payload: { target: string; type: string }) => {
      const { data } = await apiClient.post<{ data: Investigation }>("/investigations", payload)
      return data.data
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["investigations"] })
    },
  })
}
