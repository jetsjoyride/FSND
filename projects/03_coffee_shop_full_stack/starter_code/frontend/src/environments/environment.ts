/* DONE! - @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'fsnd-jps.us.auth0.com', // the auth0 domain prefix
    audience: 'coffee', // the audience set for the auth0 app
    clientId: 'wMHcXMd9ghrhywxF2ec89Kj8MPIa204b', // the client id generated for the auth0 app
    // callbackURL: 'http://localhost:8100', // the base url of the running ionic application.
    callbackURL: 'http://127.0.0.1:8100', // the base url of the running ionic application.
  }
};
