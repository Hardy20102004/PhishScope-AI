import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from "recharts"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/Card"

const data = [
  { name: "High Risk", value: 45, color: "#ef4444" },
  { name: "Medium Risk", value: 30, color: "#f59e0b" },
  { name: "Low Risk", value: 15, color: "#eab308" },
  { name: "Clean", value: 10, color: "#22c55e" },
]

export function RiskDistributionChart() {
  return (
    <Card className="flex flex-col">
      <CardHeader className="pb-2">
        <CardTitle>Risk Distribution</CardTitle>
        <CardDescription>Investigations analyzed over the last 30 days.</CardDescription>
      </CardHeader>
      <CardContent className="flex-1 pb-0">
        <div className="h-[250px] w-full">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={data}
                cx="50%"
                cy="50%"
                innerRadius={60}
                outerRadius={80}
                paddingAngle={2}
                dataKey="value"
              >
                {data.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip 
                contentStyle={{ borderRadius: "8px", border: "1px solid #e2e8f0", boxShadow: "0 4px 6px -1px rgb(0 0 0 / 0.1)" }}
                itemStyle={{ color: "#0f172a", fontWeight: 500 }}
              />
              <Legend verticalAlign="bottom" height={36} />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </CardContent>
    </Card>
  )
}
