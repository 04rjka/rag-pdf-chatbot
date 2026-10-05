"use client"
import { useTheme } from "next-themes"
import { SidebarMenuButton } from "@/components/ui/sidebar"
import { Sun, Moon } from "lucide-react"

export function ThemeToggle() {
  const { theme, setTheme } = useTheme()
  return (
    <SidebarMenuButton onClick={() => setTheme(theme === "dark" ? "light" : "dark")}>
      <Sun className="size-4 dark:hidden" />
      <Moon className="size-4 hidden dark:block" />
      Toggle theme
    </SidebarMenuButton>
  )
}