import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useNavigate, Link } from "react-router-dom";
import { ShieldCheck } from "lucide-react";
import type { RegisterFormValues } from "../../features/auth/schemas";
import { registerSchema } from "../../features/auth/schemas";
import { apiClient } from "../../api/client";
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from "../../components/ui/Card";
import { Button } from "../../components/ui/Button";
import { Input } from "../../components/ui/Input";

export default function Register() {
  const navigate = useNavigate();
  const [serverError, setServerError] = useState<string | null>(null);
  const [isSuccess, setIsSuccess] = useState(false);

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<RegisterFormValues>({
    resolver: zodResolver(registerSchema),
  });

  const onSubmit = async (data: RegisterFormValues) => {
    try {
      setServerError(null);
      await apiClient.post("/auth/register", data);
      setIsSuccess(true);
    } catch (err: any) {
      if (err.response?.data?.error?.message) {
        setServerError(err.response.data.error.message);
      } else if (err.response?.data?.detail) {
        setServerError(err.response.data.detail);
      } else {
        setServerError("Registration failed. Please try again.");
      }
    }
  };

  if (isSuccess) {
    return (
      <div className="flex h-screen items-center justify-center bg-background">
        <Card className="w-[400px]">
          <CardHeader className="text-center">
            <div className="mx-auto mb-4 bg-green-500/10 p-3 rounded-full w-fit text-green-500">
              <ShieldCheck size={32} />
            </div>
            <CardTitle className="text-2xl font-bold">Account Created</CardTitle>
            <CardDescription>Your account has been registered successfully.</CardDescription>
          </CardHeader>
          <CardContent className="text-center">
            <p className="mb-6 text-sm text-muted-foreground">
              Please check your email to verify your account before logging in.
            </p>
            <Button className="w-full" onClick={() => navigate("/login")}>
              Proceed to Login
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="flex h-screen items-center justify-center bg-background">
      <Card className="w-[400px]">
        <CardHeader className="text-center">
          <CardTitle className="text-2xl font-bold">Request Access</CardTitle>
          <CardDescription>Create your PHOENIX analyst account.</CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
            {serverError && (
              <div className="p-3 bg-destructive/15 text-destructive rounded-md text-sm">
                {serverError}
              </div>
            )}
            <div className="space-y-2">
              <label className="text-sm font-medium">Full Name</label>
              <Input
                placeholder="Jane Doe"
                {...register("full_name")}
              />
              {errors.full_name && (
                <p className="text-sm text-destructive">{errors.full_name.message}</p>
              )}
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium">Email</label>
              <Input
                type="email"
                placeholder="analyst@phoenix.io"
                {...register("email")}
              />
              {errors.email && (
                <p className="text-sm text-destructive">{errors.email.message}</p>
              )}
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium">Password</label>
              <Input
                type="password"
                {...register("password")}
              />
              {errors.password && (
                <p className="text-sm text-destructive">{errors.password.message}</p>
              )}
            </div>
            <Button className="w-full" type="submit" disabled={isSubmitting}>
              {isSubmitting ? "Registering..." : "Create Account"}
            </Button>
          </form>
        </CardContent>
        <CardFooter className="justify-center">
          <p className="text-sm text-muted-foreground">
            Already have an account?{" "}
            <Link to="/login" className="text-primary hover:underline font-medium">
              Sign In
            </Link>
          </p>
        </CardFooter>
      </Card>
    </div>
  );
}
