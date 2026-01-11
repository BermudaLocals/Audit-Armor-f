export const metadata = {
  title: 'Audit Armor',
  description: 'Security audit dashboard',
}

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
