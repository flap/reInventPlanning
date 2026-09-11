import {
  CognitoUserPool,
  CognitoUser,
  AuthenticationDetails,
  CognitoUserAttribute,
  type CognitoUserSession,
} from 'amazon-cognito-identity-js'

/**
 * Real Amazon Cognito auth (SRP flow — password never leaves the browser in
 * plaintext). Active when VITE_COGNITO_* env vars are present. See ADR-008.
 */

const REGION = import.meta.env.VITE_COGNITO_REGION as string | undefined
const USER_POOL_ID = import.meta.env.VITE_COGNITO_USER_POOL_ID as string | undefined
const CLIENT_ID = import.meta.env.VITE_COGNITO_APP_CLIENT_ID as string | undefined

export const cognitoEnabled = Boolean(REGION && USER_POOL_ID && CLIENT_ID)

let pool: CognitoUserPool | null = null
function userPool(): CognitoUserPool {
  if (!pool) {
    if (!USER_POOL_ID || !CLIENT_ID) throw new Error('Cognito not configured')
    pool = new CognitoUserPool({ UserPoolId: USER_POOL_ID, ClientId: CLIENT_ID })
  }
  return pool
}

export interface CognitoTokens {
  idToken: string
  accessToken: string
  sub: string
  email: string
}

function tokensFromSession(session: CognitoUserSession): CognitoTokens {
  const idToken = session.getIdToken()
  const payload = idToken.decodePayload()
  return {
    idToken: idToken.getJwtToken(),
    accessToken: session.getAccessToken().getJwtToken(),
    sub: String(payload.sub),
    email: String(payload.email ?? ''),
  }
}

export const cognito = {
  enabled: cognitoEnabled,

  signUp(email: string, password: string): Promise<void> {
    return new Promise((resolve, reject) => {
      const attrs = [new CognitoUserAttribute({ Name: 'email', Value: email })]
      userPool().signUp(email, password, attrs, [], (err) => {
        if (err) reject(err)
        else resolve()
      })
    })
  },

  confirm(email: string, code: string): Promise<void> {
    return new Promise((resolve, reject) => {
      const user = new CognitoUser({ Username: email, Pool: userPool() })
      user.confirmRegistration(code, true, (err) => {
        if (err) reject(err)
        else resolve()
      })
    })
  },

  resendCode(email: string): Promise<void> {
    return new Promise((resolve, reject) => {
      const user = new CognitoUser({ Username: email, Pool: userPool() })
      user.resendConfirmationCode((err) => (err ? reject(err) : resolve()))
    })
  },

  signIn(email: string, password: string): Promise<CognitoTokens> {
    return new Promise((resolve, reject) => {
      const user = new CognitoUser({ Username: email, Pool: userPool() })
      const details = new AuthenticationDetails({ Username: email, Password: password })
      user.authenticateUser(details, {
        onSuccess: (session) => resolve(tokensFromSession(session)),
        onFailure: (err) => reject(err),
      })
    })
  },

  /** Current session tokens if a valid session exists (refreshes if needed). */
  currentTokens(): Promise<CognitoTokens | null> {
    return new Promise((resolve) => {
      const user = userPool().getCurrentUser()
      if (!user) {
        resolve(null)
        return
      }
      user.getSession((err: Error | null, session: CognitoUserSession | null) => {
        if (err || !session || !session.isValid()) {
          resolve(null)
          return
        }
        resolve(tokensFromSession(session))
      })
    })
  },

  signOut(): void {
    const user = userPool().getCurrentUser()
    if (user) user.signOut()
  },
}
