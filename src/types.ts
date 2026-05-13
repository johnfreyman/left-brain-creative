export type SessionType = 'Practice' | 'Optional Training'

export interface Player {
  id: string
  name: string
  number: string
}

export interface AttendanceRecord {
  id: string
  playerId: string
  sessionType: SessionType
  date: string
  durationHours: number
}

export interface TeamSettings {
  name: string
  logoUrl: string | null
  primaryColor: string
  secondaryColor: string
  textColor: string
}
