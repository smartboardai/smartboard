import { ss } from '@/utils/storage'

const LOCAL_NAME = 'settingsStorage'

export interface SettingsState {
  systemMessage: string
  temperature: number
  top_p: number
  isEmojis?:boolean
  settings?:PublicApp.AppSetting
  privacyPolicyEn:string
  privacyPolicyAr:string
  termsOfUseEn?: string
  termsOfUseAr?: string
}

export function defaultSetting(): SettingsState {
  return {
    systemMessage: '',
    temperature: 0.8,
    top_p: 1,
    isEmojis:false,
    privacyPolicyEn:'',
    privacyPolicyAr:''
  }
}

export function getLocalState(): SettingsState {
  const localSetting: SettingsState | undefined = ss.get(LOCAL_NAME)
  return { ...defaultSetting(), ...localSetting }
}

export function setLocalState(setting: SettingsState): void {
  ss.set(LOCAL_NAME, setting)
}

export function removeLocalState() {
  ss.remove(LOCAL_NAME)
}
