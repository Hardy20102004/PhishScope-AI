import { useState } from "react"
import { useNavigate } from "react-router-dom"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import * as z from "zod"
import { Search, Link2, Mail, AlertCircle, MessageSquare, QrCode, Upload } from "lucide-react"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/Card"
import { Button } from "@/components/ui/Button"
import { Input } from "@/components/ui/Input"
import { useSubmitInvestigation } from "@/features/investigations/api/investigations"

const schema = z.object({
  target: z.string().min(1, "Target is required"),
  type: z.enum(["URL", "WEBSITE", "EMAIL", "MESSAGING", "QR", "FILE"]),
  raw_content: z.string().optional()
})

type FormData = z.infer<typeof schema>

export default function NewInvestigation() {
  const navigate = useNavigate()
  const { mutateAsync: submitScan, isPending } = useSubmitInvestigation()
  const [error, setError] = useState<string | null>(null)

  const {
    register,
    handleSubmit,
    setValue,
    watch,
    formState: { errors },
  } = useForm<FormData>({
    resolver: zodResolver(schema),
    defaultValues: { type: "URL" },
  })

  // eslint-disable-next-line react-hooks/incompatible-library
  const currentType = watch("type")

  const onSubmit = async (data: FormData) => {
    setError(null)
    try {
      const investigation = await submitScan(data)
      navigate(`/investigations/${investigation.id}`)
    } catch (err: any) {
      setError(err.response?.data?.error?.message || "An unexpected error occurred.")
    }
  }

  return (
    <div className="p-6 sm:p-8 max-w-[800px] mx-auto space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">New Investigation</h1>
        <p className="text-muted-foreground">Submit a new artifact to the engine for deep analysis.</p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Artifact Details</CardTitle>
          <CardDescription>Select the type of artifact and provide the target.</CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
            
            <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
              <button
                type="button"
                onClick={() => setValue("type", "URL")}
                className={`flex flex-col items-center justify-center p-4 border rounded-lg transition-colors ${
                  currentType === "URL" ? "border-primary bg-primary/10 text-primary" : "hover:bg-accent"
                }`}
              >
                <Link2 className="h-6 w-6 mb-2" />
                <span className="font-medium text-xs">URL</span>
              </button>

              <button
                type="button"
                onClick={() => setValue("type", "WEBSITE")}
                className={`flex flex-col items-center justify-center p-4 border rounded-lg transition-colors ${
                  currentType === "WEBSITE" ? "border-primary bg-primary/10 text-primary" : "hover:bg-accent"
                }`}
              >
                <Link2 className="h-6 w-6 mb-2" />
                <span className="font-medium text-xs">Website</span>
              </button>
              
              <button
                type="button"
                onClick={() => setValue("type", "EMAIL")}
                className={`flex flex-col items-center justify-center p-4 border rounded-lg transition-colors ${
                  currentType === "EMAIL" ? "border-primary bg-primary/10 text-primary" : "hover:bg-accent"
                }`}
              >
                <Mail className="h-6 w-6 mb-2" />
                <span className="font-medium text-xs">Email</span>
              </button>
              
              <button
                type="button"
                onClick={() => setValue("type", "MESSAGING")}
                className={`flex flex-col items-center justify-center p-4 border rounded-lg transition-colors ${
                  currentType === "MESSAGING" ? "border-primary bg-primary/10 text-primary" : "hover:bg-accent"
                }`}
              >
                <MessageSquare className="h-6 w-6 mb-2" />
                <span className="font-medium text-xs">SMS / Text</span>
              </button>
              
              <button
                type="button"
                onClick={() => setValue("type", "QR")}
                className={`flex flex-col items-center justify-center p-4 border rounded-lg transition-colors ${
                  currentType === "QR" ? "border-primary bg-primary/10 text-primary" : "hover:bg-accent"
                }`}
              >
                <QrCode className="h-6 w-6 mb-2" />
                <span className="font-medium text-xs">QR Code</span>
              </button>
            </div>

            {currentType !== "QR" && (
              <div className="space-y-2">
                <label className="text-sm font-medium">Target / Description</label>
                <div className="relative">
                  <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                  <Input 
                    {...register("target")} 
                    className="pl-10" 
                    placeholder={currentType === "EMAIL" || currentType === "MESSAGING" ? "e.g. Suspicious Phishing Attempt" : "https://suspicious-login.com"} 
                    autoComplete="off"
                  />
                </div>
                {errors.target && <p className="text-sm text-destructive">{errors.target.message}</p>}
              </div>
            )}
            
            {currentType === "QR" && (
               <div className="space-y-2 relative">
                  <label className="text-sm font-medium">Upload QR Image</label>
                  <div className="border-2 border-dashed rounded-lg p-8 flex flex-col items-center justify-center text-center cursor-pointer hover:bg-muted/50 transition-colors relative">
                     <Upload className="h-8 w-8 text-muted-foreground mb-4" />
                     <p className="text-sm text-muted-foreground mb-2">Drag and drop or click to upload</p>
                     <input 
                       type="file" 
                       accept="image/*"
                       className="w-full h-full opacity-0 absolute cursor-pointer inset-0"
                       onChange={(e) => {
                         const file = e.target.files?.[0];
                         if (file) {
                           setValue("target", file.name);
                           const reader = new FileReader();
                           reader.onloadend = () => {
                             setValue("raw_content", reader.result as string);
                           };
                           reader.readAsDataURL(file);
                         }
                       }}
                     />
                     <Input type="hidden" {...register("target")} />
                     <Input type="hidden" {...register("raw_content")} />
                  </div>
                  {watch("target") && currentType === "QR" && (
                    <p className="text-sm text-primary flex items-center gap-2 mt-2">
                      <QrCode className="h-4 w-4" /> Selected: {watch("target")}
                    </p>
                  )}
                  {errors.target && <p className="text-sm text-destructive">QR image is required.</p>}
               </div>
            )}

            {(currentType === "EMAIL" || currentType === "MESSAGING") && (
               <div className="space-y-2">
                 <label className="text-sm font-medium">Raw {currentType === "EMAIL" ? "Email (.eml)" : "Message text"}</label>
                 <textarea 
                   {...register("raw_content")}
                   className="flex min-h-[200px] w-full rounded-md border border-input bg-transparent px-3 py-2 text-sm shadow-sm placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50 font-mono"
                   placeholder={`Paste raw ${currentType === "EMAIL" ? "email headers and body" : "SMS or WhatsApp message text"} here...`}
                 />
                 {errors.raw_content && <p className="text-sm text-destructive">{errors.raw_content.message}</p>}
               </div>
            )}

            {error && (
              <div className="rounded-md bg-destructive/15 p-3 flex items-start gap-3 border border-destructive/30">
                <AlertCircle className="h-5 w-5 text-destructive shrink-0 mt-0.5" />
                <div className="text-sm text-destructive font-medium">{error}</div>
              </div>
            )}

            <div className="flex justify-end gap-3 pt-4 border-t">
              <Button type="button" variant="outline" onClick={() => navigate("/dashboard")}>Cancel</Button>
              <Button type="submit" disabled={isPending}>
                {isPending ? "Scanning..." : "Launch Investigation"}
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  )
}
