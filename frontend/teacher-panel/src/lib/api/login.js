export const login = async ({authHeader}) => {
    if (!authHeader || !authHeader.startsWith('Basic ')) {
        return new Response(JSON.stringify({ 
            message: 'Authorization header missing or not Basic' 
        }), { status: 401 });
    }

    const base64Credentials = authHeader.split(' ')[1];
    const credentials = Buffer.from(base64Credentials, 'base64').toString('ascii');
    const [username, password] = credentials.split(':');
    
    if (!username || !password) {
        return new Response(JSON.stringify({
            body: { error: 'Username and password are required' }
        }), { status: 400 });
    }
    
    const params = new URLSearchParams();
    params.append('client_id', 'svelte-teacher'); //TODO Perhaps teacher-api ???
    params.append('grant_type', 'password');
    params.append('username', username);
    params.append('password', password);

//     Token endpoint
// /realms/{realm-name}/protocol/openid-connect/token
// The token endpoint is used to obtain tokens. Tokens can either be obtained by exchanging an authorization code or by supplying credentials directly depending on what flow is used. The token endpoint is also used to obtain new access tokens when they expire.
// For more details, see the Token Endpoint section in the OpenID Connect specification. (https://openid.net/specs/openid-connect-core-1_0.html#TokenEndpoint)



    const response = await fetch(`http://keycloak:8080/realms/DM885/protocol/openid-connect/token`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: params
    });

    if (!response.ok) {
        const error = await response.json();
        return new Response(JSON.stringify({
            status: response.status,
            body: error
        }), { status: response.status });
    }

    const data = await response.json();
    return new Response(JSON.stringify({
        body: { authtoken: data.access_token }
    }), { status: 200 });
};