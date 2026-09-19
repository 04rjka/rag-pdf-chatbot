import { api } from "@/lib/api";
import { LoginFormValues } from "@/lib/schemas/login-schema"

export async function loginUser(data:LoginFormValues){
    const response = await api.post("/auth/login",data)
    
    return response
}