import { api } from "@/lib/api";
import { LoginFormValues } from "@/lib/schemas/login-schema"
import { SignupFormValues } from "@/lib/schemas/signup-schema"

export async function loginUser(data:LoginFormValues){
    const response = await api.post("/auth/login",data)
    
    return response
}

export async function signupUser(data:SignupFormValues) {
    const response = await api.post("/auth/register",data)
    return response
}