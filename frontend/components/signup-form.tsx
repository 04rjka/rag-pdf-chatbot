"use client"

import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { signupSchema, SignupFormValues } from "@/lib/schemas/signup-schema"
import Link from "next/link"
import { useRouter } from "next/navigation"

import { signupUser } from "@/lib/services/auth"

import { Button } from "@/components/ui/button"
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import {
  Field,
  FieldDescription,
  FieldGroup,
  FieldLabel,
} from "@/components/ui/field"
import { Input } from "@/components/ui/input"

export function SignupForm({ ...props }: React.ComponentProps<typeof Card>) {

  const router = useRouter()
  const {
      register,
      handleSubmit,
      formState: { errors, isSubmitting },
      setError,
    } = useForm<SignupFormValues>({
      resolver: zodResolver(signupSchema),
      defaultValues: { name : "", email: "", password: "" ,confirmPassword: ""},
    })

  async function onSubmit(values:SignupFormValues) {
    console.log(values)
    try{
        const response = await signupUser(values)
        console.log("SignUp successful : ",response.data) 
        router.push("/login")
    }catch(err:any){
      const errorMessage = err?.response?.data?.detail || "Signup Failed"
      setError("root", {message : errorMessage})
    }
  }
  return (
    <Card {...props}>
      <CardHeader>
        <CardTitle>Create an account</CardTitle>
        <CardDescription>
          Enter your information below to create your account
        </CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit(onSubmit)} noValidate>
          <FieldGroup>
            <Field>
              <FieldLabel htmlFor="name">Full Name</FieldLabel>
              <Input id="name" type="text" placeholder="John Doe" {...register("name")} />
              {errors.name && (
                  <p className="text-sm text-destructive">{errors.name.message}</p>
                )}
            </Field>
            <Field>
              <FieldLabel htmlFor="email">Email</FieldLabel>
              <Input
                id="email"
                type="email"
                placeholder="m@example.com"
                {...register("email")}
              />
              {errors.email && (
                  <p className="text-sm text-destructive">{errors.email.message}</p>
                )}
              <FieldDescription>
                We&apos;ll use this to contact you. We will not share your email
                with anyone else.
              </FieldDescription>
            </Field>
            <Field>
              <FieldLabel htmlFor="password">Password</FieldLabel>
              <Input id="password" type="password" {...register("password")} />
              {errors.password && (
                  <p className="text-sm text-destructive">{errors.password.message}</p>
                )}
              <FieldDescription>
                Must be at least 8 characters long.
              </FieldDescription>
            </Field>
            <Field>
              <FieldLabel htmlFor="confirmPassword">
                Confirm Password
              </FieldLabel>
              <Input id="confirmPassword" type="password" {...register("confirmPassword")} />
              {errors.confirmPassword && (
                  <p className="text-sm text-destructive">{errors.confirmPassword.message}</p>
                )}
              <FieldDescription>Please confirm your password.</FieldDescription>
            </Field>
            <FieldGroup>
              <Field>
                <Button type="submit" disabled={isSubmitting}>{ isSubmitting? "Signing Up" :"Sign Up"}</Button>
                {errors.root && (
                  <p className="text-sm text-destructive text-center">
                    {errors.root.message}
                  </p>
                )}
                <FieldDescription className="px-6 text-center">
                  Already have an account? <Link href="/login">Sign in</Link>
                </FieldDescription>
              </Field>
            </FieldGroup>
          </FieldGroup>
        </form>
      </CardContent>
    </Card>
  )
}
