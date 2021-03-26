/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'fsnd-3-cafe.us', // the auth0 domain prefix
    audience: 'fullstack-cafe', // the audience set for the auth0 app
    clientId: 'yxBoW4EjReQn08kcOVgRT6g7Z1UUfAGF', // the client id generated for the auth0 app
    callbackURL: 'http://127.0.0.1:8100', // the base url of the running ionic application. 
  }
};
