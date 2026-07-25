import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useNavigate, Link } from "react-router-dom";
import { LogIn } from "lucide-react";
import type { LoginFormValues } from "../../features/auth/schemas";
import { loginSchema } from "../../features/auth/schemas";
import { apiClient } from "../../api/client";
import { useAuthStore } from "../../stores/authStore";
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from "../../components/ui/Card";
import { Button } from "../../components/ui/Button";
import { Input } from "../../components/ui/Input";

export default function Login() {
  const navigate = useNavigate();
  const setAccessToken = useAuthStore((state) => state.setAccessToken);
  const [serverError, setServerError] = useState<string | null>(null);

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<LoginFormValues>({
    resolver: zodResolver(loginSchema),
  });

  const onSubmit = async (data: LoginFormValues) => {
    try {
      setServerError(null);
      
      // We must send form data for OAuth2PasswordRequestForm in FastAPI
      const formData = new URLSearchParams();
      formData.append("username", data.email);
      formData.append("password", data.password);

      const res = await apiClient.post("/auth/login", formData, {
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
      });
      
      const accessToken = res.data.data.access_token;
      setAccessToken(accessToken);
      
      // Navigate to dashboard where /users/me will fetch profile
      navigate("/dashboard");
    } catch (err: any) {
      if (err.response?.data?.error?.message) {
        setServerError(err.response.data.error.message);
      } else if (err.response?.data?.detail) {
        setServerError(err.response.data.detail);
      } else {
        setServerError("An unexpected error occurred. Please try again.");
      }
    }
  };

  return (
    <div className="flex h-screen items-center justify-center bg-background">
      <Card className="w-[400px]">
        <CardHeader className="text-center">
          <div className="mx-auto mb-4 bg-primary/10 p-3 rounded-full w-fit text-primary">
            <LogIn size={32} />
          </div>
          <CardTitle className="text-2xl font-bold">Welcome Back</CardTitle>
          <CardDescription>Enter your credentials to access PHOENIX.</CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
            {serverError && (
              <div className="p-3 bg-destructive/15 text-destructive rounded-md text-sm">
                {serverError}
              </div>
            )}
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
              <div className="flex items-center justify-between">
                <label className="text-sm font-medium">Password</label>
                <Link to="/forgot-password" className="text-sm text-primary hover:underline">
                  Forgot password?
                </Link>
              </div>
              <Input
                type="password"
                {...register("password")}
              />
              {errors.password && (
                <p className="text-sm text-destructive">{errors.password.message}</p>
              )}
            </div>
            <Button className="w-full" type="submit" disabled={isSubmitting}>
              {isSubmitting ? "Authenticating..." : "Sign In"}
            </Button>
          </form>
        </CardContent>
        <CardFooter className="justify-center">
          <p className="text-sm text-muted-foreground">
            Don't have an account?{" "}
            <Link to="/register" className="text-primary hover:underline font-medium">
              Request Access
            </Link>
          </p>
        </CardFooter>
      </Card>
    </div>
  );
}
