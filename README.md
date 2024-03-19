<div align="left">

[![Visit Launchdarkly](./header.png)](https://launchdarkly.com)

# Launchdarkly<a id="launchdarkly"></a>

# Overview<a id="overview"></a>

## Authentication<a id="authentication"></a>

LaunchDarkly's REST API uses the HTTPS protocol with a minimum TLS version of 1.2.

All REST API resources are authenticated with either [personal or service access tokens](https://docs.launchdarkly.com/home/account-security/api-access-tokens), or session cookies. Other authentication mechanisms are not supported. You can manage personal access tokens on your [**Account settings**](https://app.launchdarkly.com/settings/tokens) page.

LaunchDarkly also has SDK keys, mobile keys, and client-side IDs that are used by our server-side SDKs, mobile SDKs, and JavaScript-based SDKs, respectively. **These keys cannot be used to access our REST API**. These keys are environment-specific, and can only perform read-only operations such as fetching feature flag settings.

| Auth mechanism                                                                                  | Allowed resources                                                                                     | Use cases                                          |
| ----------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- | -------------------------------------------------- |
| [Personal or service access tokens](https://docs.launchdarkly.com/home/account-security/api-access-tokens) | Can be customized on a per-token basis                                                                | Building scripts, custom integrations, data export. |
| SDK keys                                                                                        | Can only access read-only resources specific to server-side SDKs. Restricted to a single environment. | Server-side SDKs                     |
| Mobile keys                                                                                     | Can only access read-only resources specific to mobile SDKs, and only for flags marked available to mobile keys. Restricted to a single environment.           | Mobile SDKs                                        |
| Client-side ID                                                                                  | Can only access read-only resources specific to JavaScript-based client-side SDKs, and only for flags marked available to client-side. Restricted to a single environment.           | Client-side JavaScript                             |

> #### Keep your access tokens and SDK keys private
>
> Access tokens should _never_ be exposed in untrusted contexts. Never put an access token in client-side JavaScript, or embed it in a mobile application. LaunchDarkly has special mobile keys that you can embed in mobile apps. If you accidentally expose an access token or SDK key, you can reset it from your [**Account settings**](https://app.launchdarkly.com/settings/tokens) page.
>
> The client-side ID is safe to embed in untrusted contexts. It's designed for use in client-side JavaScript.

### Authentication using request header<a id="authentication-using-request-header"></a>

The preferred way to authenticate with the API is by adding an `Authorization` header containing your access token to your requests. The value of the `Authorization` header must be your access token.

Manage personal access tokens from the [**Account settings**](https://app.launchdarkly.com/settings/tokens) page.

### Authentication using session cookie<a id="authentication-using-session-cookie"></a>

For testing purposes, you can make API calls directly from your web browser. If you are logged in to the LaunchDarkly application, the API will use your existing session to authenticate calls.

If you have a [role](https://docs.launchdarkly.com/home/team/built-in-roles) other than Admin, or have a [custom role](https://docs.launchdarkly.com/home/team/custom-roles) defined, you may not have permission to perform some API calls. You will receive a `401` response code in that case.

> ### Modifying the Origin header causes an error
>
> LaunchDarkly validates that the Origin header for any API request authenticated by a session cookie matches the expected Origin header. The expected Origin header is `https://app.launchdarkly.com`.
>
> If the Origin header does not match what's expected, LaunchDarkly returns an error. This error can prevent the LaunchDarkly app from working correctly.
>
> Any browser extension that intentionally changes the Origin header can cause this problem. For example, the `Allow-Control-Allow-Origin: *` Chrome extension changes the Origin header to `http://evil.com` and causes the app to fail.
>
> To prevent this error, do not modify your Origin header.
>
> LaunchDarkly does not require origin matching when authenticating with an access token, so this issue does not affect normal API usage.

## Representations<a id="representations"></a>

All resources expect and return JSON response bodies. Error responses also send a JSON body. To learn more about the error format of the API, read [Errors](https://apidocs.launchdarkly.com).

In practice this means that you always get a response with a `Content-Type` header set to `application/json`.

In addition, request bodies for `PATCH`, `POST`, and `PUT` requests must be encoded as JSON with a `Content-Type` header set to `application/json`.

### Summary and detailed representations<a id="summary-and-detailed-representations"></a>

When you fetch a list of resources, the response includes only the most important attributes of each resource. This is a _summary representation_ of the resource. When you fetch an individual resource, such as a single feature flag, you receive a _detailed representation_ of the resource.

The best way to find a detailed representation is to follow links. Every summary representation includes a link to its detailed representation.

### Expanding responses<a id="expanding-responses"></a>

Sometimes the detailed representation of a resource does not include all of the attributes of the resource by default. If this is the case, the request method will clearly document this and describe which attributes you can include in an expanded response.

To include the additional attributes, append the `expand` request parameter to your request and add a comma-separated list of the attributes to include. For example, when you append `?expand=members,roles` to the [Get team](https://apidocs.launchdarkly.com) endpoint, the expanded response includes both of these attributes.

### Links and addressability<a id="links-and-addressability"></a>

The best way to navigate the API is by following links. These are attributes in representations that link to other resources. The API always uses the same format for links:

- Links to other resources within the API are encapsulated in a `_links` object
- If the resource has a corresponding link to HTML content on the site, it is stored in a special `_site` link

Each link has two attributes:

- An `href`, which contains the URL
- A `type`, which describes the content type

For example, a feature resource might return the following:

```json
{
  \"_links\": {
    \"parent\": {
      \"href\": \"/api/features\",
      \"type\": \"application/json\"
    },
    \"self\": {
      \"href\": \"/api/features/sort.order\",
      \"type\": \"application/json\"
    }
  },
  \"_site\": {
    \"href\": \"/features/sort.order\",
    \"type\": \"text/html\"
  }
}
```

From this, you can navigate to the parent collection of features by following the `parent` link, or navigate to the site page for the feature by following the `_site` link.

Collections are always represented as a JSON object with an `items` attribute containing an array of representations. Like all other representations, collections have `_links` defined at the top level.

Paginated collections include `first`, `last`, `next`, and `prev` links containing a URL with the respective set of elements in the collection.

## Updates<a id="updates"></a>

Resources that accept partial updates use the `PATCH` verb. Most resources support the [JSON patch](https://apidocs.launchdarkly.com) format. Some resources also support the [JSON merge patch](https://apidocs.launchdarkly.com) format, and some resources support the [semantic patch](https://apidocs.launchdarkly.com) format, which is a way to specify the modifications to perform as a set of executable instructions. Each resource supports optional [comments](https://apidocs.launchdarkly.com) that you can submit with updates. Comments appear in outgoing webhooks, the audit log, and other integrations.

When a resource supports both JSON patch and semantic patch, we document both in the request method. However, the specific request body fields and descriptions included in our documentation only match one type of patch or the other.

### Updates using JSON patch<a id="updates-using-json-patch"></a>

[JSON patch](https://datatracker.ietf.org/doc/html/rfc6902) is a way to specify the modifications to perform on a resource. JSON patch uses paths and a limited set of operations to describe how to transform the current state of the resource into a new state. JSON patch documents are always arrays, where each element contains an operation, a path to the field to update, and the new value.

For example, in this feature flag representation:

```json
{
    \"name\": \"New recommendations engine\",
    \"key\": \"engine.enable\",
    \"description\": \"This is the description\",
    ...
}
```
You can change the feature flag's description with the following patch document:

```json
[{ \"op\": \"replace\", \"path\": \"/description\", \"value\": \"This is the new description\" }]
```

You can specify multiple modifications to perform in a single request. You can also test that certain preconditions are met before applying the patch:

```json
[
  { \"op\": \"test\", \"path\": \"/version\", \"value\": 10 },
  { \"op\": \"replace\", \"path\": \"/description\", \"value\": \"The new description\" }
]
```

The above patch request tests whether the feature flag's `version` is `10`, and if so, changes the feature flag's description.

Attributes that are not editable, such as a resource's `_links`, have names that start with an underscore.

### Updates using JSON merge patch<a id="updates-using-json-merge-patch"></a>

[JSON merge patch](https://datatracker.ietf.org/doc/html/rfc7386) is another format for specifying the modifications to perform on a resource. JSON merge patch is less expressive than JSON patch. However, in many cases it is simpler to construct a merge patch document. For example, you can change a feature flag's description with the following merge patch document:

```json
{
  \"description\": \"New flag description\"
}
```

### Updates using semantic patch<a id="updates-using-semantic-patch"></a>

Some resources support the semantic patch format. A semantic patch is a way to specify the modifications to perform on a resource as a set of executable instructions.

Semantic patch allows you to be explicit about intent using precise, custom instructions. In many cases, you can define semantic patch instructions independently of the current state of the resource. This can be useful when defining a change that may be applied at a future date.

To make a semantic patch request, you must append `domain-model=launchdarkly.semanticpatch` to your `Content-Type` header.

Here's how:

```
Content-Type: application/json; domain-model=launchdarkly.semanticpatch
```

If you call a semantic patch resource without this header, you will receive a `400` response because your semantic patch will be interpreted as a JSON patch.

The body of a semantic patch request takes the following properties:

* `comment` (string): (Optional) A description of the update.
* `environmentKey` (string): (Required for some resources only) The environment key.
* `instructions` (array): (Required) A list of actions the update should perform. Each action in the list must be an object with a `kind` property that indicates the instruction. If the instruction requires parameters, you must include those parameters as additional fields in the object. The documentation for each resource that supports semantic patch includes the available instructions and any additional parameters.

For example:

```json
{
  \"comment\": \"optional comment\",
  \"instructions\": [ {\"kind\": \"turnFlagOn\"} ]
}
```

If any instruction in the patch encounters an error, the endpoint returns an error and will not change the resource. In general, each instruction silently does nothing if the resource is already in the state you request.

### Updates with comments<a id="updates-with-comments"></a>

You can submit optional comments with `PATCH` changes.

To submit a comment along with a JSON patch document, use the following format:

```json
{
  \"comment\": \"This is a comment string\",
  \"patch\": [{ \"op\": \"replace\", \"path\": \"/description\", \"value\": \"The new description\" }]
}
```

To submit a comment along with a JSON merge patch document, use the following format:

```json
{
  \"comment\": \"This is a comment string\",
  \"merge\": { \"description\": \"New flag description\" }
}
```

To submit a comment along with a semantic patch, use the following format:

```json
{
  \"comment\": \"This is a comment string\",
  \"instructions\": [ {\"kind\": \"turnFlagOn\"} ]
}
```

## Errors<a id="errors"></a>

The API always returns errors in a common format. Here's an example:

```json
{
  \"code\": \"invalid_request\",
  \"message\": \"A feature with that key already exists\",
  \"id\": \"30ce6058-87da-11e4-b116-123b93f75cba\"
}
```

The `code` indicates the general class of error. The `message` is a human-readable explanation of what went wrong. The `id` is a unique identifier. Use it when you're working with LaunchDarkly Support to debug a problem with a specific API call.

### HTTP status error response codes<a id="http-status-error-response-codes"></a>

| Code | Definition        | Description                                                                                       | Possible Solution                                                |
| ---- | ----------------- | ------------------------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| 400  | Invalid request       | The request cannot be understood.                                    | Ensure JSON syntax in request body is correct.                   |
| 401  | Invalid access token      | Requestor is unauthorized or does not have permission for this API call.                                                | Ensure your API access token is valid and has the appropriate permissions.                                     |
| 403  | Forbidden         | Requestor does not have access to this resource.                                                | Ensure that the account member or access token has proper permissions set. |
| 404  | Invalid resource identifier | The requested resource is not valid. | Ensure that the resource is correctly identified by ID or key. |
| 405  | Method not allowed | The request method is not allowed on this resource. | Ensure that the HTTP verb is correct. |
| 409  | Conflict          | The API request can not be completed because it conflicts with a concurrent API request. | Retry your request.                                              |
| 422  | Unprocessable entity | The API request can not be completed because the update description can not be understood. | Ensure that the request body is correct for the type of patch you are using, either JSON patch or semantic patch.
| 429  | Too many requests | Read [Rate limiting](https://apidocs.launchdarkly.com).                                               | Wait and try again later.                                        |

## CORS<a id="cors"></a>

The LaunchDarkly API supports Cross Origin Resource Sharing (CORS) for AJAX requests from any origin. If an `Origin` header is given in a request, it will be echoed as an explicitly allowed origin. Otherwise the request returns a wildcard, `Access-Control-Allow-Origin: *`. For more information on CORS, read the [CORS W3C Recommendation](http://www.w3.org/TR/cors). Example CORS headers might look like:

```http
Access-Control-Allow-Headers: Accept, Content-Type, Content-Length, Accept-Encoding, Authorization
Access-Control-Allow-Methods: OPTIONS, GET, DELETE, PATCH
Access-Control-Allow-Origin: *
Access-Control-Max-Age: 300
```

You can make authenticated CORS calls just as you would make same-origin calls, using either [token or session-based authentication](https://apidocs.launchdarkly.com). If you are using session authentication, you should set the `withCredentials` property for your `xhr` request to `true`. You should never expose your access tokens to untrusted entities.

## Rate limiting<a id="rate-limiting"></a>

We use several rate limiting strategies to ensure the availability of our APIs. Rate-limited calls to our APIs return a `429` status code. Calls to our APIs include headers indicating the current rate limit status. The specific headers returned depend on the API route being called. The limits differ based on the route, authentication mechanism, and other factors. Routes that are not rate limited may not contain any of the headers described below.

> ### Rate limiting and SDKs
>
> LaunchDarkly SDKs are never rate limited and do not use the API endpoints defined here. LaunchDarkly uses a different set of approaches, including streaming/server-sent events and a global CDN, to ensure availability to the routes used by LaunchDarkly SDKs.

### Global rate limits<a id="global-rate-limits"></a>

Authenticated requests are subject to a global limit. This is the maximum number of calls that your account can make to the API per ten seconds. All service and personal access tokens on the account share this limit, so exceeding the limit with one access token will impact other tokens. Calls that are subject to global rate limits may return the headers below:

| Header name                    | Description                                                                      |
| ------------------------------ | -------------------------------------------------------------------------------- |
| `X-Ratelimit-Global-Remaining` | The maximum number of requests the account is permitted to make per ten seconds. |
| `X-Ratelimit-Reset`            | The time at which the current rate limit window resets in epoch milliseconds.    |

We do not publicly document the specific number of calls that can be made globally. This limit may change, and we encourage clients to program against the specification, relying on the two headers defined above, rather than hardcoding to the current limit.

### Route-level rate limits<a id="route-level-rate-limits"></a>

Some authenticated routes have custom rate limits. These also reset every ten seconds. Any service or personal access tokens hitting the same route share this limit, so exceeding the limit with one access token may impact other tokens. Calls that are subject to route-level rate limits return the headers below:

| Header name                   | Description                                                                                           |
| ----------------------------- | ----------------------------------------------------------------------------------------------------- |
| `X-Ratelimit-Route-Remaining` | The maximum number of requests to the current route the account is permitted to make per ten seconds. |
| `X-Ratelimit-Reset`           | The time at which the current rate limit window resets in epoch milliseconds.                         |

A _route_ represents a specific URL pattern and verb. For example, the [Delete environment](https://apidocs.launchdarkly.com) endpoint is considered a single route, and each call to delete an environment counts against your route-level rate limit for that route.

We do not publicly document the specific number of calls that an account can make to each endpoint per ten seconds. These limits may change, and we encourage clients to program against the specification, relying on the two headers defined above, rather than hardcoding to the current limits.

### IP-based rate limiting<a id="ip-based-rate-limiting"></a>

We also employ IP-based rate limiting on some API routes. If you hit an IP-based rate limit, your API response will include a `Retry-After` header indicating how long to wait before re-trying the call. Clients must wait at least `Retry-After` seconds before making additional calls to our API, and should employ jitter and backoff strategies to avoid triggering rate limits again.

## OpenAPI (Swagger) and client libraries<a id="openapi-swagger-and-client-libraries"></a>

We have a [complete OpenAPI (Swagger) specification](https://app.launchdarkly.com/api/v2/openapi.json) for our API.

We auto-generate multiple client libraries based on our OpenAPI specification. To learn more, visit the [collection of client libraries on GitHub](https://github.com/search?q=topic%3Alaunchdarkly-api+org%3Alaunchdarkly&type=Repositories). You can also use this specification to generate client libraries to interact with our REST API in your language of choice.

Our OpenAPI specification is supported by several API-based tools such as Postman and Insomnia. In many cases, you can directly import our specification to explore our APIs.

## Method overriding<a id="method-overriding"></a>

Some firewalls and HTTP clients restrict the use of verbs other than `GET` and `POST`. In those environments, our API endpoints that use `DELETE`, `PATCH`, and `PUT` verbs are inaccessible.

To avoid this issue, our API supports the `X-HTTP-Method-Override` header, allowing clients to \"tunnel\" `DELETE`, `PATCH`, and `PUT` requests using a `POST` request.

For example, to call a `PATCH` endpoint using a `POST` request, you can include `X-HTTP-Method-Override:PATCH` as a header.

## Beta resources<a id="beta-resources"></a>

We sometimes release new API resources in **beta** status before we release them with general availability.

Resources that are in beta are still undergoing testing and development. They may change without notice, including becoming backwards incompatible.

We try to promote resources into general availability as quickly as possible. This happens after sufficient testing and when we're satisfied that we no longer need to make backwards-incompatible changes.

We mark beta resources with a \"Beta\" callout in our documentation, pictured below:

> ### This feature is in beta
>
> To use this feature, pass in a header including the `LD-API-Version` key with value set to `beta`. Use this header with each call. To learn more, read [Beta resources](https://apidocs.launchdarkly.com).
>
> Resources that are in beta are still undergoing testing and development. They may change without notice, including becoming backwards incompatible.

### Using beta resources<a id="using-beta-resources"></a>

To use a beta resource, you must include a header in the request. If you call a beta resource without this header, you receive a `403` response.

Use this header:

```
LD-API-Version: beta
```

## Federal environments<a id="federal-environments"></a>

The version of LaunchDarkly that is available on domains controlled by the United States government is different from the version of LaunchDarkly available to the general public. If you are an employee or contractor for a United States federal agency and use LaunchDarkly in your work, you likely use the federal instance of LaunchDarkly.

If you are working in the federal instance of LaunchDarkly, the base URI for each request is `https://app.launchdarkly.us`. In the \"Try it\" sandbox for each request, click the request path to view the complete resource path for the federal environment.

To learn more, read [LaunchDarkly in federal environments](https://docs.launchdarkly.com/home/advanced/federal).

## Versioning<a id="versioning"></a>

We try hard to keep our REST API backwards compatible, but we occasionally have to make backwards-incompatible changes in the process of shipping new features. These breaking changes can cause unexpected behavior if you don't prepare for them accordingly.

Updates to our REST API include support for the latest features in LaunchDarkly. We also release a new version of our REST API every time we make a breaking change. We provide simultaneous support for multiple API versions so you can migrate from your current API version to a new version at your own pace.

### Setting the API version per request<a id="setting-the-api-version-per-request"></a>

You can set the API version on a specific request by sending an `LD-API-Version` header, as shown in the example below:

```
LD-API-Version: 20220603
```

The header value is the version number of the API version you would like to request. The number for each version corresponds to the date the version was released in `yyyymmdd` format. In the example above the version `20220603` corresponds to June 03, 2022.

### Setting the API version per access token<a id="setting-the-api-version-per-access-token"></a>

When you create an access token, you must specify a specific version of the API to use. This ensures that integrations using this token cannot be broken by version changes.

Tokens created before versioning was released have their version set to `20160426`, which is the version of the API that existed before the current versioning scheme, so that they continue working the same way they did before versioning.

If you would like to upgrade your integration to use a new API version, you can explicitly set the header described above.

> ### Best practice: Set the header for every client or integration
>
> We recommend that you set the API version header explicitly in any client or integration you build.
>
> Only rely on the access token API version during manual testing.

### API version changelog<a id="api-version-changelog"></a>

|<div style=\"width:75px\">Version</div> | Changes | End of life (EOL)
|---|---|---|
| `20220603` | <ul><li>Changed the [list projects](https://apidocs.launchdarkly.com) return value:<ul><li>Response is now paginated with a default limit of `20`.</li><li>Added support for filter and sort.</li><li>The project `environments` field is now expandable. This field is omitted by default.</li></ul></li><li>Changed the [get project](https://apidocs.launchdarkly.com) return value:<ul><li>The `environments` field is now expandable. This field is omitted by default.</li></ul></li></ul> | Current |
| `20210729` | <ul><li>Changed the [create approval request](https://apidocs.launchdarkly.com) return value. It now returns HTTP Status Code `201` instead of `200`.</li><li> Changed the [get users](https://apidocs.launchdarkly.com) return value. It now returns a user record, not a user. </li><li>Added additional optional fields to environment, segments, flags, members, and segments, including the ability to create big segments. </li><li> Added default values for flag variations when new environments are created. </li><li>Added filtering and pagination for getting flags and members, including `limit`, `number`, `filter`, and `sort` query parameters. </li><li>Added endpoints for expiring user targets for flags and segments, scheduled changes, access tokens, Relay Proxy configuration, integrations and subscriptions, and approvals. </li></ul> | 2023-06-03 |
| `20191212` | <ul><li>[List feature flags](https://apidocs.launchdarkly.com) now defaults to sending summaries of feature flag configurations, equivalent to setting the query parameter `summary=true`. Summaries omit flag targeting rules and individual user targets from the payload. </li><li> Added endpoints for flags, flag status, projects, environments, audit logs, members, users, custom roles, segments, usage, streams, events, and data export. </li></ul> | 2022-07-29 |
| `20160426` | <ul><li>Initial versioning of API. Tokens created before versioning have their version set to this.</li></ul> | 2020-12-12 |



</div>

## Table of Contents<a id="table-of-contents"></a>

<!-- toc -->

- [Requirements](#requirements)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Async](#async)
- [Raw HTTP Response](#raw-http-response)
- [Reference](#reference)
  * [`launchdarkly.access_tokens.create_new_token`](#launchdarklyaccess_tokenscreate_new_token)
  * [`launchdarkly.access_tokens.delete_by_id`](#launchdarklyaccess_tokensdelete_by_id)
  * [`launchdarkly.access_tokens.get_by_id`](#launchdarklyaccess_tokensget_by_id)
  * [`launchdarkly.access_tokens.list`](#launchdarklyaccess_tokenslist)
  * [`launchdarkly.access_tokens.reset_secret_key`](#launchdarklyaccess_tokensreset_secret_key)
  * [`launchdarkly.access_tokens.update_settings`](#launchdarklyaccess_tokensupdate_settings)
  * [`launchdarkly.account_members.add_to_teams`](#launchdarklyaccount_membersadd_to_teams)
  * [`launchdarkly.account_members.delete_by_id`](#launchdarklyaccount_membersdelete_by_id)
  * [`launchdarkly.account_members.get_by_id`](#launchdarklyaccount_membersget_by_id)
  * [`launchdarkly.account_members.invite_new_members`](#launchdarklyaccount_membersinvite_new_members)
  * [`launchdarkly.account_members.list_members`](#launchdarklyaccount_memberslist_members)
  * [Filtering members](#filtering-members)
  * [Sorting members](#sorting-members)
  * [`launchdarkly.account_members.update_member_patch`](#launchdarklyaccount_membersupdate_member_patch)
  * [`launchdarkly.account_members_(beta).modify_members_roles`](#launchdarklyaccount_members_betamodify_members_roles)
  * [Full use of this API resource is an Enterprise feature](#full-use-of-this-api-resource-is-an-enterprise-feature)
  * [Instructions](#instructions)
  * [`launchdarkly.account_usage_(beta).get_evaluations_usage`](#launchdarklyaccount_usage_betaget_evaluations_usage)
  * [`launchdarkly.account_usage_(beta).get_events_usage_data`](#launchdarklyaccount_usage_betaget_events_usage_data)
  * [`launchdarkly.account_usage_(beta).get_experimentation_keys_usage`](#launchdarklyaccount_usage_betaget_experimentation_keys_usage)
  * [`launchdarkly.account_usage_(beta).get_experimentation_units_usage`](#launchdarklyaccount_usage_betaget_experimentation_units_usage)
  * [`launchdarkly.account_usage_(beta).get_mau_usage_by_category`](#launchdarklyaccount_usage_betaget_mau_usage_by_category)
  * [`launchdarkly.account_usage_(beta).get_mau_usage_data`](#launchdarklyaccount_usage_betaget_mau_usage_data)
  * [`launchdarkly.account_usage_(beta).get_stream_usage`](#launchdarklyaccount_usage_betaget_stream_usage)
  * [`launchdarkly.account_usage_(beta).get_stream_usage_by_sdk_version_data`](#launchdarklyaccount_usage_betaget_stream_usage_by_sdk_version_data)
  * [`launchdarkly.account_usage_(beta).list_mau_sdks_by_type`](#launchdarklyaccount_usage_betalist_mau_sdks_by_type)
  * [`launchdarkly.account_usage_(beta).list_sdk_versions`](#launchdarklyaccount_usage_betalist_sdk_versions)
  * [`launchdarkly.applications_(beta).get_application_by_key`](#launchdarklyapplications_betaget_application_by_key)
  * [Expanding the application response](#expanding-the-application-response)
  * [`launchdarkly.applications_(beta).get_application_versions`](#launchdarklyapplications_betaget_application_versions)
  * [`launchdarkly.applications_(beta).list_applications`](#launchdarklyapplications_betalist_applications)
  * [Expanding the applications response](#expanding-the-applications-response)
  * [`launchdarkly.applications_(beta).remove_application`](#launchdarklyapplications_betaremove_application)
  * [`launchdarkly.applications_(beta).remove_version`](#launchdarklyapplications_betaremove_version)
  * [`launchdarkly.applications_(beta).update_application_patch`](#launchdarklyapplications_betaupdate_application_patch)
  * [`launchdarkly.applications_(beta).update_version_patch`](#launchdarklyapplications_betaupdate_version_patch)
  * [`launchdarkly.approvals.apply_request_flag`](#launchdarklyapprovalsapply_request_flag)
  * [`launchdarkly.approvals.apply_request_flag_0`](#launchdarklyapprovalsapply_request_flag_0)
  * [`launchdarkly.approvals.create_flag_copy_request`](#launchdarklyapprovalscreate_flag_copy_request)
  * [`launchdarkly.approvals.create_request_flag`](#launchdarklyapprovalscreate_request_flag)
  * [`launchdarkly.approvals.create_request_flag_0`](#launchdarklyapprovalscreate_request_flag_0)
  * [`launchdarkly.approvals.delete_approval_request_flag`](#launchdarklyapprovalsdelete_approval_request_flag)
  * [`launchdarkly.approvals.delete_request`](#launchdarklyapprovalsdelete_request)
  * [`launchdarkly.approvals.get_request_by_id`](#launchdarklyapprovalsget_request_by_id)
  * [Expanding approval response](#expanding-approval-response)
  * [`launchdarkly.approvals.list`](#launchdarklyapprovalslist)
  * [Filtering approvals](#filtering-approvals)
  * [Expanding approval response](#expanding-approval-response-1)
  * [`launchdarkly.approvals.list_requests_for_flag`](#launchdarklyapprovalslist_requests_for_flag)
  * [`launchdarkly.approvals.review_flag_request`](#launchdarklyapprovalsreview_flag_request)
  * [`launchdarkly.approvals.review_request`](#launchdarklyapprovalsreview_request)
  * [`launchdarkly.approvals.single_request`](#launchdarklyapprovalssingle_request)
  * [`launchdarkly.audit_log.detail_entry`](#launchdarklyaudit_logdetail_entry)
  * [`launchdarkly.audit_log.list_audit_log_entries`](#launchdarklyaudit_loglist_audit_log_entries)
  * [`launchdarkly.code_references.asynchronously_delete_branches`](#launchdarklycode_referencesasynchronously_delete_branches)
  * [`launchdarkly.code_references.create_extinction`](#launchdarklycode_referencescreate_extinction)
  * [`launchdarkly.code_references.create_repository`](#launchdarklycode_referencescreate_repository)
  * [`launchdarkly.code_references.delete_repository`](#launchdarklycode_referencesdelete_repository)
  * [`launchdarkly.code_references.get_branch`](#launchdarklycode_referencesget_branch)
  * [`launchdarkly.code_references.get_repository_by_repo`](#launchdarklycode_referencesget_repository_by_repo)
  * [`launchdarkly.code_references.get_statistics`](#launchdarklycode_referencesget_statistics)
  * [`launchdarkly.code_references.get_statistics_0`](#launchdarklycode_referencesget_statistics_0)
  * [`launchdarkly.code_references.list_branches`](#launchdarklycode_referenceslist_branches)
  * [`launchdarkly.code_references.list_extinctions`](#launchdarklycode_referenceslist_extinctions)
  * [`launchdarkly.code_references.list_repositories`](#launchdarklycode_referenceslist_repositories)
  * [`launchdarkly.code_references.update_repository_settings`](#launchdarklycode_referencesupdate_repository_settings)
  * [`launchdarkly.code_references.upsert_branch`](#launchdarklycode_referencesupsert_branch)
  * [`launchdarkly.context_settings.update_settings_for_context`](#launchdarklycontext_settingsupdate_settings_for_context)
  * [`launchdarkly.contexts.create_or_update_kind`](#launchdarklycontextscreate_or_update_kind)
  * [`launchdarkly.contexts.delete_context_instance`](#launchdarklycontextsdelete_context_instance)
  * [`launchdarkly.contexts.evaluate_flags_for_context_instance`](#launchdarklycontextsevaluate_flags_for_context_instance)
  * [Filtering](#filtering)
  * [`launchdarkly.contexts.get_attribute_names`](#launchdarklycontextsget_attribute_names)
  * [`launchdarkly.contexts.get_by_kind_and_key`](#launchdarklycontextsget_by_kind_and_key)
  * [`launchdarkly.contexts.get_context_attribute_values`](#launchdarklycontextsget_context_attribute_values)
  * [`launchdarkly.contexts.get_context_instances`](#launchdarklycontextsget_context_instances)
  * [`launchdarkly.contexts.list_context_kinds_by_project`](#launchdarklycontextslist_context_kinds_by_project)
  * [`launchdarkly.contexts.search_context_instances`](#launchdarklycontextssearch_context_instances)
  * [`launchdarkly.contexts.search_contexts`](#launchdarklycontextssearch_contexts)
  * [`launchdarkly.custom_roles.create_new_role`](#launchdarklycustom_rolescreate_new_role)
  * [`launchdarkly.custom_roles.delete_role_by_custom_key`](#launchdarklycustom_rolesdelete_role_by_custom_key)
  * [`launchdarkly.custom_roles.get_by_custom_key`](#launchdarklycustom_rolesget_by_custom_key)
  * [`launchdarkly.custom_roles.list_custom_roles`](#launchdarklycustom_roleslist_custom_roles)
  * [`launchdarkly.custom_roles.update_single_custom_role`](#launchdarklycustom_rolesupdate_single_custom_role)
  * [`launchdarkly.data_export_destinations.create_destination`](#launchdarklydata_export_destinationscreate_destination)
  * [`launchdarkly.data_export_destinations.delete_by_id`](#launchdarklydata_export_destinationsdelete_by_id)
  * [`launchdarkly.data_export_destinations.get_all`](#launchdarklydata_export_destinationsget_all)
  * [`launchdarkly.data_export_destinations.get_single_by_id`](#launchdarklydata_export_destinationsget_single_by_id)
  * [`launchdarkly.data_export_destinations.update_destination_patch`](#launchdarklydata_export_destinationsupdate_destination_patch)
  * [`launchdarkly.environments.create_new_environment`](#launchdarklyenvironmentscreate_new_environment)
  * [Approval settings](#approval-settings)
  * [`launchdarkly.environments.get_by_project_and_key`](#launchdarklyenvironmentsget_by_project_and_key)
  * [Approval settings](#approval-settings-1)
  * [`launchdarkly.environments.list_environments`](#launchdarklyenvironmentslist_environments)
  * [Filtering environments](#filtering-environments)
  * [Sorting environments](#sorting-environments)
  * [`launchdarkly.environments.remove_by_environment_key`](#launchdarklyenvironmentsremove_by_environment_key)
  * [`launchdarkly.environments.reset_mobile_sdk_key`](#launchdarklyenvironmentsreset_mobile_sdk_key)
  * [`launchdarkly.environments.reset_sdk_key`](#launchdarklyenvironmentsreset_sdk_key)
  * [`launchdarkly.environments.update_environment_patch`](#launchdarklyenvironmentsupdate_environment_patch)
  * [Approval settings](#approval-settings-2)
  * [`launchdarkly.experiments_(beta).create_iteration`](#launchdarklyexperiments_betacreate_iteration)
  * [`launchdarkly.experiments_(beta).create_new`](#launchdarklyexperiments_betacreate_new)
  * [`launchdarkly.experiments_(beta).get_details`](#launchdarklyexperiments_betaget_details)
  * [Expanding the experiment response](#expanding-the-experiment-response)
  * [`launchdarkly.experiments_(beta).get_experiment_metric_results`](#launchdarklyexperiments_betaget_experiment_metric_results)
  * [`launchdarkly.experiments_(beta).get_experimentation_settings`](#launchdarklyexperiments_betaget_experimentation_settings)
  * [`launchdarkly.experiments_(beta).get_legacy_experiment_results`](#launchdarklyexperiments_betaget_legacy_experiment_results)
  * [`launchdarkly.experiments_(beta).get_results_for_metric_group`](#launchdarklyexperiments_betaget_results_for_metric_group)
  * [`launchdarkly.experiments_(beta).list_experiments_in_environment`](#launchdarklyexperiments_betalist_experiments_in_environment)
  * [Filtering experiments](#filtering-experiments)
  * [Expanding the experiments response](#expanding-the-experiments-response)
  * [`launchdarkly.experiments_(beta).update_experimentation_settings`](#launchdarklyexperiments_betaupdate_experimentation_settings)
  * [`launchdarkly.experiments_(beta).update_semantic_patch`](#launchdarklyexperiments_betaupdate_semantic_patch)
  * [Instructions](#instructions-1)
  * [`launchdarkly.feature_flags.across_environments`](#launchdarklyfeature_flagsacross_environments)
  * [`launchdarkly.feature_flags.copy_flag_settings`](#launchdarklyfeature_flagscopy_flag_settings)
  * [Copying flag settings is an Enterprise feature](#copying-flag-settings-is-an-enterprise-feature)
  * [`launchdarkly.feature_flags.create_feature_flag`](#launchdarklyfeature_flagscreate_feature_flag)
  * [Creating a migration flag](#creating-a-migration-flag)
  * [`launchdarkly.feature_flags.delete_flag`](#launchdarklyfeature_flagsdelete_flag)
  * [`launchdarkly.feature_flags.get_context_instance_segments_membership_by_env`](#launchdarklyfeature_flagsget_context_instance_segments_membership_by_env)
  * [`launchdarkly.feature_flags.get_status`](#launchdarklyfeature_flagsget_status)
  * [`launchdarkly.feature_flags.list`](#launchdarklyfeature_flagslist)
  * [Filtering flags](#filtering-flags)
  * [Sorting flags](#sorting-flags)
  * [Expanding response](#expanding-response)
  * [Migration flags](#migration-flags)
  * [`launchdarkly.feature_flags.list_expiring_user_targets`](#launchdarklyfeature_flagslist_expiring_user_targets)
  * [Contexts are now available](#contexts-are-now-available)
  * [`launchdarkly.feature_flags.list_flag_statuses`](#launchdarklyfeature_flagslist_flag_statuses)
  * [`launchdarkly.feature_flags.single_flag_by_key`](#launchdarklyfeature_flagssingle_flag_by_key)
  * [Expanding response](#expanding-response-1)
  * [`launchdarkly.feature_flags.update_expiring_context_targets`](#launchdarklyfeature_flagsupdate_expiring_context_targets)
  * [Instructions](#instructions-2)
  * [`launchdarkly.feature_flags.update_expiring_user_targets`](#launchdarklyfeature_flagsupdate_expiring_user_targets)
  * [Contexts are now available](#contexts-are-now-available-1)
  * [Instructions](#instructions-3)
  * [`launchdarkly.feature_flags.update_feature_flag`](#launchdarklyfeature_flagsupdate_feature_flag)
  * [Using semantic patches on a feature flag](#using-semantic-patches-on-a-feature-flag)
  * [Instructions](#instructions-4)
  * [Using JSON patches on a feature flag](#using-json-patches-on-a-feature-flag)
  * [Required approvals](#required-approvals)
  * [Conflicts](#conflicts)
  * [Migration flags](#migration-flags-1)
  * [`launchdarkly.feature_flags_(beta).get_migration_safety_issues`](#launchdarklyfeature_flags_betaget_migration_safety_issues)
  * [`launchdarkly.feature_flags_(beta).list_dependent_flags`](#launchdarklyfeature_flags_betalist_dependent_flags)
  * [Flag prerequisites is an Enterprise feature](#flag-prerequisites-is-an-enterprise-feature)
  * [`launchdarkly.feature_flags_(beta).list_dependent_flags_by_env`](#launchdarklyfeature_flags_betalist_dependent_flags_by_env)
  * [Flag prerequisites is an Enterprise feature](#flag-prerequisites-is-an-enterprise-feature-1)
  * [`launchdarkly.flag_links_(beta).create_flag_link`](#launchdarklyflag_links_betacreate_flag_link)
  * [`launchdarkly.flag_links_(beta).delete_flag_link`](#launchdarklyflag_links_betadelete_flag_link)
  * [`launchdarkly.flag_links_(beta).list_links`](#launchdarklyflag_links_betalist_links)
  * [`launchdarkly.flag_links_(beta).update_flag_link`](#launchdarklyflag_links_betaupdate_flag_link)
  * [`launchdarkly.flag_triggers.create_trigger_workflow`](#launchdarklyflag_triggerscreate_trigger_workflow)
  * [`launchdarkly.flag_triggers.delete_by_id`](#launchdarklyflag_triggersdelete_by_id)
  * [`launchdarkly.flag_triggers.get_trigger_by_id`](#launchdarklyflag_triggersget_trigger_by_id)
  * [`launchdarkly.flag_triggers.list_trigger_workflows`](#launchdarklyflag_triggerslist_trigger_workflows)
  * [`launchdarkly.flag_triggers.update_trigger_workflow_patch`](#launchdarklyflag_triggersupdate_trigger_workflow_patch)
  * [Instructions](#instructions-5)
  * [`launchdarkly.follow_flags.flag_followers_list`](#launchdarklyfollow_flagsflag_followers_list)
  * [`launchdarkly.follow_flags.get_all_flag_followers`](#launchdarklyfollow_flagsget_all_flag_followers)
  * [`launchdarkly.follow_flags.member_follower`](#launchdarklyfollow_flagsmember_follower)
  * [`launchdarkly.follow_flags.remove_follower`](#launchdarklyfollow_flagsremove_follower)
  * [`launchdarkly.insights_charts_(beta).deployment_frequency_chart_data`](#launchdarklyinsights_charts_betadeployment_frequency_chart_data)
  * [Expanding the chart response](#expanding-the-chart-response)
  * [`launchdarkly.insights_charts_(beta).get_flag_status_chart_data`](#launchdarklyinsights_charts_betaget_flag_status_chart_data)
  * [`launchdarkly.insights_charts_(beta).lead_time_chart_data`](#launchdarklyinsights_charts_betalead_time_chart_data)
  * [`launchdarkly.insights_charts_(beta).release_frequency_data`](#launchdarklyinsights_charts_betarelease_frequency_data)
  * [`launchdarkly.insights_charts_(beta).stale_flags_chart_data`](#launchdarklyinsights_charts_betastale_flags_chart_data)
  * [Expanding the chart response](#expanding-the-chart-response-1)
  * [`launchdarkly.insights_deployments_(beta).create_deployment_event`](#launchdarklyinsights_deployments_betacreate_deployment_event)
  * [`launchdarkly.insights_deployments_(beta).get_deployment_by_id`](#launchdarklyinsights_deployments_betaget_deployment_by_id)
  * [Expanding the deployment response](#expanding-the-deployment-response)
  * [`launchdarkly.insights_deployments_(beta).list_deployments`](#launchdarklyinsights_deployments_betalist_deployments)
  * [Expanding the deployment collection response](#expanding-the-deployment-collection-response)
  * [`launchdarkly.insights_deployments_(beta).update_deployment_by_id`](#launchdarklyinsights_deployments_betaupdate_deployment_by_id)
  * [`launchdarkly.insights_flag_events_(beta).list_flag_events`](#launchdarklyinsights_flag_events_betalist_flag_events)
  * [Expanding the flag event collection response](#expanding-the-flag-event-collection-response)
  * [`launchdarkly.insights_pull_requests_(beta).list_pull_requests`](#launchdarklyinsights_pull_requests_betalist_pull_requests)
  * [Expanding the pull request collection response](#expanding-the-pull-request-collection-response)
  * [`launchdarkly.insights_repositories_(beta).associate_repositories_and_projects`](#launchdarklyinsights_repositories_betaassociate_repositories_and_projects)
  * [`launchdarkly.insights_repositories_(beta).list_repositories`](#launchdarklyinsights_repositories_betalist_repositories)
  * [Expanding the repository collection response](#expanding-the-repository-collection-response)
  * [`launchdarkly.insights_repositories_(beta).remove_repository_project_association`](#launchdarklyinsights_repositories_betaremove_repository_project_association)
  * [`launchdarkly.insights_scores_(beta).create_insight_group`](#launchdarklyinsights_scores_betacreate_insight_group)
  * [`launchdarkly.insights_scores_(beta).delete_insight_group`](#launchdarklyinsights_scores_betadelete_insight_group)
  * [`launchdarkly.insights_scores_(beta).expand_group_insight_scores`](#launchdarklyinsights_scores_betaexpand_group_insight_scores)
  * [Expanding the insight group response](#expanding-the-insight-group-response)
  * [`launchdarkly.insights_scores_(beta).get_insight_scores`](#launchdarklyinsights_scores_betaget_insight_scores)
  * [`launchdarkly.insights_scores_(beta).list_group_insight_scores`](#launchdarklyinsights_scores_betalist_group_insight_scores)
  * [Expanding the insight groups collection response](#expanding-the-insight-groups-collection-response)
  * [`launchdarkly.insights_scores_(beta).update_insight_group_patch`](#launchdarklyinsights_scores_betaupdate_insight_group_patch)
  * [`launchdarkly.integration_audit_log_subscriptions.create_subscription`](#launchdarklyintegration_audit_log_subscriptionscreate_subscription)
  * [`launchdarkly.integration_audit_log_subscriptions.delete_subscription`](#launchdarklyintegration_audit_log_subscriptionsdelete_subscription)
  * [`launchdarkly.integration_audit_log_subscriptions.get_by_id`](#launchdarklyintegration_audit_log_subscriptionsget_by_id)
  * [`launchdarkly.integration_audit_log_subscriptions.list_by_integration`](#launchdarklyintegration_audit_log_subscriptionslist_by_integration)
  * [`launchdarkly.integration_audit_log_subscriptions.update_subscription`](#launchdarklyintegration_audit_log_subscriptionsupdate_subscription)
  * [`launchdarkly.integration_delivery_configurations_(beta).create_delivery_configuration`](#launchdarklyintegration_delivery_configurations_betacreate_delivery_configuration)
  * [`launchdarkly.integration_delivery_configurations_(beta).delete_delivery_configuration`](#launchdarklyintegration_delivery_configurations_betadelete_delivery_configuration)
  * [`launchdarkly.integration_delivery_configurations_(beta).get_by_id`](#launchdarklyintegration_delivery_configurations_betaget_by_id)
  * [`launchdarkly.integration_delivery_configurations_(beta).get_delivery_configurations_by_environment`](#launchdarklyintegration_delivery_configurations_betaget_delivery_configurations_by_environment)
  * [`launchdarkly.integration_delivery_configurations_(beta).list_delivery_configurations`](#launchdarklyintegration_delivery_configurations_betalist_delivery_configurations)
  * [`launchdarkly.integration_delivery_configurations_(beta).update_delivery_configuration`](#launchdarklyintegration_delivery_configurations_betaupdate_delivery_configuration)
  * [`launchdarkly.integration_delivery_configurations_(beta).validate_delivery_configuration`](#launchdarklyintegration_delivery_configurations_betavalidate_delivery_configuration)
  * [`launchdarkly.integrations_(beta).create_persistent_store_integration`](#launchdarklyintegrations_betacreate_persistent_store_integration)
  * [`launchdarkly.integrations_(beta).delete_big_segment_store_integration`](#launchdarklyintegrations_betadelete_big_segment_store_integration)
  * [`launchdarkly.integrations_(beta).get_big_segment_store_integration_by_id`](#launchdarklyintegrations_betaget_big_segment_store_integration_by_id)
  * [`launchdarkly.integrations_(beta).list_big_segment_store_integrations`](#launchdarklyintegrations_betalist_big_segment_store_integrations)
  * [`launchdarkly.integrations_(beta).update_big_segment_store`](#launchdarklyintegrations_betaupdate_big_segment_store)
  * [`launchdarkly.metrics.create_new_metric`](#launchdarklymetricscreate_new_metric)
  * [`launchdarkly.metrics.delete_by_project_and_metric_key`](#launchdarklymetricsdelete_by_project_and_metric_key)
  * [`launchdarkly.metrics.get_single_metric`](#launchdarklymetricsget_single_metric)
  * [Expanding the metric response](#expanding-the-metric-response)
  * [`launchdarkly.metrics.list_for_project`](#launchdarklymetricslist_for_project)
  * [Expanding the metric list response](#expanding-the-metric-list-response)
  * [`launchdarkly.metrics.update_by_json_patch`](#launchdarklymetricsupdate_by_json_patch)
  * [`launchdarkly.metrics_(beta).create_metric_group`](#launchdarklymetrics_betacreate_metric_group)
  * [`launchdarkly.metrics_(beta).delete_metric_group`](#launchdarklymetrics_betadelete_metric_group)
  * [`launchdarkly.metrics_(beta).get_metric_group_details`](#launchdarklymetrics_betaget_metric_group_details)
  * [Expanding the metric group response](#expanding-the-metric-group-response)
  * [`launchdarkly.metrics_(beta).list_metric_groups`](#launchdarklymetrics_betalist_metric_groups)
  * [Expanding the metric groups response](#expanding-the-metric-groups-response)
  * [`launchdarkly.metrics_(beta).update_metric_group_by_key`](#launchdarklymetrics_betaupdate_metric_group_by_key)
  * [`launchdarkly.o_auth2_clients.create_client`](#launchdarklyo_auth2_clientscreate_client)
  * [`launchdarkly.o_auth2_clients.delete_client_by_id`](#launchdarklyo_auth2_clientsdelete_client_by_id)
  * [`launchdarkly.o_auth2_clients.get_client_by_id`](#launchdarklyo_auth2_clientsget_client_by_id)
  * [`launchdarkly.o_auth2_clients.list`](#launchdarklyo_auth2_clientslist)
  * [`launchdarkly.o_auth2_clients.update_client_by_id`](#launchdarklyo_auth2_clientsupdate_client_by_id)
  * [`launchdarkly.other.get_ip_list`](#launchdarklyotherget_ip_list)
  * [`launchdarkly.other.get_openapi_spec`](#launchdarklyotherget_openapi_spec)
  * [`launchdarkly.other.get_resource_categories`](#launchdarklyotherget_resource_categories)
  * [`launchdarkly.other.get_version_information`](#launchdarklyotherget_version_information)
  * [`launchdarkly.projects.create_new_project`](#launchdarklyprojectscreate_new_project)
  * [`launchdarkly.projects.delete_by_project_key`](#launchdarklyprojectsdelete_by_project_key)
  * [`launchdarkly.projects.get_flag_defaults`](#launchdarklyprojectsget_flag_defaults)
  * [`launchdarkly.projects.list_projects_default`](#launchdarklyprojectslist_projects_default)
  * [Filtering projects](#filtering-projects)
  * [Sorting projects](#sorting-projects)
  * [Expanding the projects response](#expanding-the-projects-response)
  * [`launchdarkly.projects.single_by_project_key`](#launchdarklyprojectssingle_by_project_key)
  * [Expanding the project response](#expanding-the-project-response)
  * [`launchdarkly.projects.update_flag_default`](#launchdarklyprojectsupdate_flag_default)
  * [`launchdarkly.projects.update_flag_defaults_for_project`](#launchdarklyprojectsupdate_flag_defaults_for_project)
  * [`launchdarkly.projects.update_project_patch`](#launchdarklyprojectsupdate_project_patch)
  * [`launchdarkly.relay_proxy_configurations.create_new_config`](#launchdarklyrelay_proxy_configurationscreate_new_config)
  * [`launchdarkly.relay_proxy_configurations.delete_by_id`](#launchdarklyrelay_proxy_configurationsdelete_by_id)
  * [`launchdarkly.relay_proxy_configurations.get_single_by_id`](#launchdarklyrelay_proxy_configurationsget_single_by_id)
  * [`launchdarkly.relay_proxy_configurations.list`](#launchdarklyrelay_proxy_configurationslist)
  * [`launchdarkly.relay_proxy_configurations.reset_secret_key_with_expiry`](#launchdarklyrelay_proxy_configurationsreset_secret_key_with_expiry)
  * [`launchdarkly.relay_proxy_configurations.update_config_patch`](#launchdarklyrelay_proxy_configurationsupdate_config_patch)
  * [`launchdarkly.release_pipelines_(beta).create_new_pipeline`](#launchdarklyrelease_pipelines_betacreate_new_pipeline)
  * [`launchdarkly.release_pipelines_(beta).delete_pipeline`](#launchdarklyrelease_pipelines_betadelete_pipeline)
  * [`launchdarkly.release_pipelines_(beta).get_all_release_pipelines`](#launchdarklyrelease_pipelines_betaget_all_release_pipelines)
  * [Filtering release pipelines](#filtering-release-pipelines)
  * [`launchdarkly.release_pipelines_(beta).get_by_pipe_key`](#launchdarklyrelease_pipelines_betaget_by_pipe_key)
  * [`launchdarkly.release_pipelines_(beta).update_pipeline_patch`](#launchdarklyrelease_pipelines_betaupdate_pipeline_patch)
  * [`launchdarkly.releases_(beta).get_current_release`](#launchdarklyreleases_betaget_current_release)
  * [`launchdarkly.releases_(beta).update_active_release_patch`](#launchdarklyreleases_betaupdate_active_release_patch)
  * [`launchdarkly.scheduled_changes.create_workflow`](#launchdarklyscheduled_changescreate_workflow)
  * [`launchdarkly.scheduled_changes.delete_workflow`](#launchdarklyscheduled_changesdelete_workflow)
  * [`launchdarkly.scheduled_changes.get_by_id`](#launchdarklyscheduled_changesget_by_id)
  * [`launchdarkly.scheduled_changes.list_changes`](#launchdarklyscheduled_changeslist_changes)
  * [`launchdarkly.scheduled_changes.update_workflow`](#launchdarklyscheduled_changesupdate_workflow)
  * [Instructions](#instructions-6)
  * [`launchdarkly.segments.create_segment`](#launchdarklysegmentscreate_segment)
  * [`launchdarkly.segments.evaluate_segment_memberships`](#launchdarklysegmentsevaluate_segment_memberships)
  * [`launchdarkly.segments.get_context_membership`](#launchdarklysegmentsget_context_membership)
  * [`launchdarkly.segments.get_expiring_targets`](#launchdarklysegmentsget_expiring_targets)
  * [`launchdarkly.segments.get_expiring_user_targets`](#launchdarklysegmentsget_expiring_user_targets)
  * [Contexts are now available](#contexts-are-now-available-2)
  * [`launchdarkly.segments.get_segment_list`](#launchdarklysegmentsget_segment_list)
  * [`launchdarkly.segments.get_user_membership_status`](#launchdarklysegmentsget_user_membership_status)
  * [Contexts are now available](#contexts-are-now-available-3)
  * [`launchdarkly.segments.remove_segment`](#launchdarklysegmentsremove_segment)
  * [`launchdarkly.segments.single_segment_by_key`](#launchdarklysegmentssingle_segment_by_key)
  * [`launchdarkly.segments.update_context_targets`](#launchdarklysegmentsupdate_context_targets)
  * [`launchdarkly.segments.update_expiring_targets_for_segment`](#launchdarklysegmentsupdate_expiring_targets_for_segment)
  * [Instructions](#instructions-7)
  * [`launchdarkly.segments.update_expiring_targets_for_segment_0`](#launchdarklysegmentsupdate_expiring_targets_for_segment_0)
  * [Contexts are now available](#contexts-are-now-available-4)
  * [Instructions](#instructions-8)
  * [`launchdarkly.segments.update_semantic_patch`](#launchdarklysegmentsupdate_semantic_patch)
  * [Using semantic patches on a segment](#using-semantic-patches-on-a-segment)
  * [Instructions](#instructions-9)
- [Using JSON patches on a segment](#using-json-patches-on-a-segment)
  * [`launchdarkly.segments.update_user_context_targets`](#launchdarklysegmentsupdate_user_context_targets)
  * [`launchdarkly.segments_(beta).get_big_segment_export_info`](#launchdarklysegments_betaget_big_segment_export_info)
  * [`launchdarkly.segments_(beta).get_import_info`](#launchdarklysegments_betaget_import_info)
  * [`launchdarkly.segments_(beta).start_big_segment_export`](#launchdarklysegments_betastart_big_segment_export)
  * [`launchdarkly.segments_(beta).start_big_segment_import`](#launchdarklysegments_betastart_big_segment_import)
  * [`launchdarkly.tags.list`](#launchdarklytagslist)
  * [`launchdarkly.teams.add_multiple_members_to_team`](#launchdarklyteamsadd_multiple_members_to_team)
  * [`launchdarkly.teams.create_team`](#launchdarklyteamscreate_team)
  * [Expanding the teams response](#expanding-the-teams-response)
  * [`launchdarkly.teams.get_by_team_key`](#launchdarklyteamsget_by_team_key)
  * [Expanding the teams response](#expanding-the-teams-response-1)
  * [`launchdarkly.teams.get_custom_roles`](#launchdarklyteamsget_custom_roles)
  * [`launchdarkly.teams.get_maintainers`](#launchdarklyteamsget_maintainers)
  * [`launchdarkly.teams.list_teams`](#launchdarklyteamslist_teams)
  * [Filtering teams](#filtering-teams)
  * [Expanding the teams response](#expanding-the-teams-response-2)
  * [`launchdarkly.teams.remove_by_team_key`](#launchdarklyteamsremove_by_team_key)
  * [`launchdarkly.teams.update_semantic_patch`](#launchdarklyteamsupdate_semantic_patch)
  * [Instructions](#instructions-10)
  * [Expanding the teams response](#expanding-the-teams-response-3)
  * [`launchdarkly.teams_(beta).update_multiple_teams_semantic_patch`](#launchdarklyteams_betaupdate_multiple_teams_semantic_patch)
  * [Instructions](#instructions-11)
  * [`launchdarkly.user_settings.get_user_expiring_flag_targets`](#launchdarklyuser_settingsget_user_expiring_flag_targets)
  * [`launchdarkly.user_settings.list_flag_settings_for_user`](#launchdarklyuser_settingslist_flag_settings_for_user)
  * [`launchdarkly.user_settings.single_flag_setting`](#launchdarklyuser_settingssingle_flag_setting)
  * [`launchdarkly.user_settings.update_expiring_user_target`](#launchdarklyuser_settingsupdate_expiring_user_target)
  * [Instructions](#instructions-12)
  * [`launchdarkly.user_settings.update_flag_settings_for_user`](#launchdarklyuser_settingsupdate_flag_settings_for_user)
  * [`launchdarkly.users.delete_by_project_environment_key`](#launchdarklyusersdelete_by_project_environment_key)
  * [Use contexts instead](#use-contexts-instead)
  * [`launchdarkly.users.get_user_by_key`](#launchdarklyusersget_user_by_key)
  * [Use contexts instead](#use-contexts-instead-1)
  * [`launchdarkly.users.list_environment_users`](#launchdarklyuserslist_environment_users)
  * [Use contexts instead](#use-contexts-instead-2)
  * [`launchdarkly.users.search_users`](#launchdarklyuserssearch_users)
  * [Use contexts instead](#use-contexts-instead-3)
  * [`launchdarkly.users_(beta).get_all_in_use_user_attributes`](#launchdarklyusers_betaget_all_in_use_user_attributes)
  * [Use contexts instead](#use-contexts-instead-4)
  * [`launchdarkly.webhooks.create_new_webhook`](#launchdarklywebhookscreate_new_webhook)
  * [`launchdarkly.webhooks.delete_by_id`](#launchdarklywebhooksdelete_by_id)
  * [`launchdarkly.webhooks.get_single_by_id`](#launchdarklywebhooksget_single_by_id)
  * [`launchdarkly.webhooks.list_webhooks`](#launchdarklywebhookslist_webhooks)
  * [`launchdarkly.webhooks.update_settings_patch`](#launchdarklywebhooksupdate_settings_patch)
  * [`launchdarkly.workflow_templates.create_feature_flag_template`](#launchdarklyworkflow_templatescreate_feature_flag_template)
  * [`launchdarkly.workflow_templates.delete_template`](#launchdarklyworkflow_templatesdelete_template)
  * [`launchdarkly.workflow_templates.list`](#launchdarklyworkflow_templateslist)
  * [`launchdarkly.workflows.create_workflow`](#launchdarklyworkflowscreate_workflow)
  * [Creating a workflow](#creating-a-workflow)
  * [Creating a workflow by applying a workflow template](#creating-a-workflow-by-applying-a-workflow-template)
  * [`launchdarkly.workflows.delete_from_feature_flag`](#launchdarklyworkflowsdelete_from_feature_flag)
  * [`launchdarkly.workflows.get_custom_workflow_by_id`](#launchdarklyworkflowsget_custom_workflow_by_id)
  * [`launchdarkly.workflows.get_feature_flag_environments_workflows`](#launchdarklyworkflowsget_feature_flag_environments_workflows)

<!-- tocstop -->

## Requirements<a id="requirements"></a>

Python >=3.7

## Installation<a id="installation"></a>
<div align="center">
  <a href="https://konfigthis.com/sdk-sign-up?company=LaunchDarkly&language=Python">
    <img src="https://raw.githubusercontent.com/konfig-dev/brand-assets/HEAD/cta-images/python-cta.png" width="70%">
  </a>
</div>

## Getting Started<a id="getting-started"></a>

```python
from pprint import pprint
from launch_darkly_python_sdk import LaunchDarkly, ApiException

launchdarkly = LaunchDarkly(

        api_key = 'YOUR_API_KEY',
)

try:
    # Create access token
    create_new_token_response = launchdarkly.access_tokens.create_new_token(
        description="string_example",
        name="string_example",
        role="reader",
        custom_role_ids=[
        "string_example"
    ],
        inline_role=[
        {
            "resources": ["proj/*:env/*:flag/*;testing-tag"],
            "actions": ["*"],
            "effect": "allow",
        }
    ],
        service_token=True,
        default_api_version=1,
    )
    print(create_new_token_response)
except ApiException as e:
    print("Exception when calling AccessTokensApi.create_new_token: %s\n" % e)
    pprint(e.body)
    if e.status == 400:
        pprint(e.body["code"])
        pprint(e.body["message"])
    if e.status == 401:
        pprint(e.body["code"])
        pprint(e.body["message"])
    if e.status == 403:
        pprint(e.body["code"])
        pprint(e.body["message"])
    if e.status == 429:
        pprint(e.body["code"])
        pprint(e.body["message"])
    pprint(e.headers)
    pprint(e.status)
    pprint(e.reason)
    pprint(e.round_trip_time)
```

## Async<a id="async"></a>

`async` support is available by prepending `a` to any method.

```python

import asyncio
from pprint import pprint
from launch_darkly_python_sdk import LaunchDarkly, ApiException

launchdarkly = LaunchDarkly(

        api_key = 'YOUR_API_KEY',
)

async def main():
    try:
        # Create access token
        create_new_token_response = await launchdarkly.access_tokens.acreate_new_token(
            description="string_example",
            name="string_example",
            role="reader",
            custom_role_ids=[
        "string_example"
    ],
            inline_role=[
        {
            "resources": ["proj/*:env/*:flag/*;testing-tag"],
            "actions": ["*"],
            "effect": "allow",
        }
    ],
            service_token=True,
            default_api_version=1,
        )
        print(create_new_token_response)
    except ApiException as e:
        print("Exception when calling AccessTokensApi.create_new_token: %s\n" % e)
        pprint(e.body)
        if e.status == 400:
            pprint(e.body["code"])
            pprint(e.body["message"])
        if e.status == 401:
            pprint(e.body["code"])
            pprint(e.body["message"])
        if e.status == 403:
            pprint(e.body["code"])
            pprint(e.body["message"])
        if e.status == 429:
            pprint(e.body["code"])
            pprint(e.body["message"])
        pprint(e.headers)
        pprint(e.status)
        pprint(e.reason)
        pprint(e.round_trip_time)

asyncio.run(main())
```

## Raw HTTP Response<a id="raw-http-response"></a>

To access raw HTTP response values, use the `.raw` namespace.

```python
from pprint import pprint
from launch_darkly_python_sdk import LaunchDarkly, ApiException

launchdarkly = LaunchDarkly(

        api_key = 'YOUR_API_KEY',
)

try:
    # Create access token
    create_new_token_response = launchdarkly.access_tokens.raw.create_new_token(
        description="string_example",
        name="string_example",
        role="reader",
        custom_role_ids=[
        "string_example"
    ],
        inline_role=[
        {
            "resources": ["proj/*:env/*:flag/*;testing-tag"],
            "actions": ["*"],
            "effect": "allow",
        }
    ],
        service_token=True,
        default_api_version=1,
    )
    pprint(create_new_token_response.body)
    pprint(create_new_token_response.body["id"])
    pprint(create_new_token_response.body["owner_id"])
    pprint(create_new_token_response.body["member_id"])
    pprint(create_new_token_response.body["creation_date"])
    pprint(create_new_token_response.body["last_modified"])
    pprint(create_new_token_response.body["links"])
    pprint(create_new_token_response.body["description"])
    pprint(create_new_token_response.body["member"])
    pprint(create_new_token_response.body["name"])
    pprint(create_new_token_response.body["custom_role_ids"])
    pprint(create_new_token_response.body["inline_role"])
    pprint(create_new_token_response.body["role"])
    pprint(create_new_token_response.body["token"])
    pprint(create_new_token_response.body["service_token"])
    pprint(create_new_token_response.body["default_api_version"])
    pprint(create_new_token_response.body["last_used"])
    pprint(create_new_token_response.headers)
    pprint(create_new_token_response.status)
    pprint(create_new_token_response.round_trip_time)
except ApiException as e:
    print("Exception when calling AccessTokensApi.create_new_token: %s\n" % e)
    pprint(e.body)
    if e.status == 400:
        pprint(e.body["code"])
        pprint(e.body["message"])
    if e.status == 401:
        pprint(e.body["code"])
        pprint(e.body["message"])
    if e.status == 403:
        pprint(e.body["code"])
        pprint(e.body["message"])
    if e.status == 429:
        pprint(e.body["code"])
        pprint(e.body["message"])
    pprint(e.headers)
    pprint(e.status)
    pprint(e.reason)
    pprint(e.round_trip_time)
```


## Reference<a id="reference"></a>
### `launchdarkly.access_tokens.create_new_token`<a id="launchdarklyaccess_tokenscreate_new_token"></a>

Create a new access token.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
create_new_token_response = launchdarkly.access_tokens.create_new_token(
    description="string_example",
    name="string_example",
    role="reader",
    custom_role_ids=[
        "string_example"
    ],
    inline_role=[
        {
            "resources": ["proj/*:env/*:flag/*;testing-tag"],
            "actions": ["*"],
            "effect": "allow",
        }
    ],
    service_token=True,
    default_api_version=1,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### description: `str`<a id="description-str"></a>

A description for the access token

##### name: `str`<a id="name-str"></a>

A human-friendly name for the access token

##### role: `str`<a id="role-str"></a>

Built-in role for the token

##### custom_role_ids: [`AccessTokenPostCustomRoleIds`](./launch_darkly_python_sdk/type/access_token_post_custom_role_ids.py)<a id="custom_role_ids-accesstokenpostcustomroleidslaunch_darkly_python_sdktypeaccess_token_post_custom_role_idspy"></a>

##### inline_role: List[`StatementPost`]<a id="inline_role-liststatementpost"></a>

A JSON array of statements represented as JSON objects with three attributes: effect, resources, actions. May be used in place of a built-in or custom role.

##### service_token: `bool`<a id="service_token-bool"></a>

Whether the token is a service token https://docs.launchdarkly.com/home/account-security/api-access-tokens#service-tokens

##### default_api_version: `int`<a id="default_api_version-int"></a>

The default API version for this token

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`AccessTokenPost`](./launch_darkly_python_sdk/type/access_token_post.py)
#### 🔄 Return<a id="🔄-return"></a>

[`Token`](./launch_darkly_python_sdk/pydantic/token.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/tokens` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.access_tokens.delete_by_id`<a id="launchdarklyaccess_tokensdelete_by_id"></a>

Delete an access token by ID.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
launchdarkly.access_tokens.delete_by_id(
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

The ID of the access token to update

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/tokens/{id}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.access_tokens.get_by_id`<a id="launchdarklyaccess_tokensget_by_id"></a>

Get a single access token by ID.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_by_id_response = launchdarkly.access_tokens.get_by_id(
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

The ID of the access token

#### 🔄 Return<a id="🔄-return"></a>

[`Token`](./launch_darkly_python_sdk/pydantic/token.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/tokens/{id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.access_tokens.list`<a id="launchdarklyaccess_tokenslist"></a>

Fetch a list of all access tokens.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_response = launchdarkly.access_tokens.list(
    show_all=True,
    limit=1,
    offset=1,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### show_all: `bool`<a id="show_all-bool"></a>

If set to true, and the authentication access token has the 'Admin' role, personal access tokens for all members will be retrieved.

##### limit: `int`<a id="limit-int"></a>

The number of access tokens to return in the response. Defaults to 25.

##### offset: `int`<a id="offset-int"></a>

Where to start in the list. This is for use with pagination. For example, an offset of 10 skips the first ten items and then returns the next items in the list, up to the query `limit`.

#### 🔄 Return<a id="🔄-return"></a>

[`Tokens`](./launch_darkly_python_sdk/pydantic/tokens.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/tokens` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.access_tokens.reset_secret_key`<a id="launchdarklyaccess_tokensreset_secret_key"></a>

Reset an access token's secret key with an optional expiry time for the old key.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
reset_secret_key_response = launchdarkly.access_tokens.reset_secret_key(
    id="id_example",
    expiry=1,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

The ID of the access token to update

##### expiry: `int`<a id="expiry-int"></a>

An expiration time for the old token key, expressed as a Unix epoch time in milliseconds. By default, the token will expire immediately.

#### 🔄 Return<a id="🔄-return"></a>

[`Token`](./launch_darkly_python_sdk/pydantic/token.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/tokens/{id}/reset` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.access_tokens.update_settings`<a id="launchdarklyaccess_tokensupdate_settings"></a>

Update an access token's settings. Updating an access token uses a [JSON patch](https://datatracker.ietf.org/doc/html/rfc6902) representation of the desired changes. To learn more, read [Updates](https://apidocs.launchdarkly.com).

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
update_settings_response = launchdarkly.access_tokens.update_settings(
    body=[{"op":"replace","path":"/role","value":"writer"}],
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

The ID of the access token to update

##### requestBody: [`JSONPatch`](./launch_darkly_python_sdk/type/json_patch.py)<a id="requestbody-jsonpatchlaunch_darkly_python_sdktypejson_patchpy"></a>

#### 🔄 Return<a id="🔄-return"></a>

[`Token`](./launch_darkly_python_sdk/pydantic/token.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/tokens/{id}` `patch`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.account_members.add_to_teams`<a id="launchdarklyaccount_membersadd_to_teams"></a>

Add one member to one or more teams.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
add_to_teams_response = launchdarkly.account_members.add_to_teams(
    team_keys=["team1", "team2"],
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### team_keys: [`MemberTeamsPostInputTeamKeys`](./launch_darkly_python_sdk/type/member_teams_post_input_team_keys.py)<a id="team_keys-memberteamspostinputteamkeyslaunch_darkly_python_sdktypemember_teams_post_input_team_keyspy"></a>

##### id: `str`<a id="id-str"></a>

The member ID

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`MemberTeamsPostInput`](./launch_darkly_python_sdk/type/member_teams_post_input.py)
#### 🔄 Return<a id="🔄-return"></a>

[`Member`](./launch_darkly_python_sdk/pydantic/member.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/members/{id}/teams` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.account_members.delete_by_id`<a id="launchdarklyaccount_membersdelete_by_id"></a>

Delete a single account member by ID. Requests to delete account members will not work if SCIM is enabled for the account.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
launchdarkly.account_members.delete_by_id(
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

The member ID

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/members/{id}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.account_members.get_by_id`<a id="launchdarklyaccount_membersget_by_id"></a>

Get a single account member by member ID.

`me` is a reserved value for the `id` parameter that returns the caller's member information.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_by_id_response = launchdarkly.account_members.get_by_id(
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

The member ID

#### 🔄 Return<a id="🔄-return"></a>

[`Member`](./launch_darkly_python_sdk/pydantic/member.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/members/{id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.account_members.invite_new_members`<a id="launchdarklyaccount_membersinvite_new_members"></a>

Invite one or more new members to join an account. Each member is sent an invitation. Members with "admin" or "owner" roles may create new members, as well as anyone with a "createMember" permission for "member/\*". If a member cannot be invited, the entire request is rejected and no members are invited from that request.

Each member _must_ have an `email` field and either a `role` or a `customRoles` field. If any of the fields are not populated correctly, the request is rejected with the reason specified in the "message" field of the response.

Requests to create account members will not work if SCIM is enabled for the account.

_No more than 50 members may be created per request._

A request may also fail because of conflicts with existing members. These conflicts are reported using the additional `code` and `invalid_emails` response fields with the following possible values for `code`:

- **email_already_exists_in_account**: A member with this email address already exists in this account.
- **email_taken_in_different_account**: A member with this email address exists in another account.
- **duplicate_email**s: This request contains two or more members with the same email address.

A request that fails for one of the above reasons returns an HTTP response code of 400 (Bad Request).


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
invite_new_members_response = launchdarkly.account_members.invite_new_members(
    body=[
        {
            "email": "sandy@acme.com",
            "password": "***",
            "first_name": "Ariel",
            "last_name": "Flores",
            "role": "reader",
            "custom_roles": ["customRole1", "customRole2"],
            "team_keys": ["team-1", "team-2"],
        }
    ],
)
```

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`NewMemberFormListPost`](./launch_darkly_python_sdk/type/new_member_form_list_post.py)
#### 🔄 Return<a id="🔄-return"></a>

[`Members`](./launch_darkly_python_sdk/pydantic/members.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/members` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.account_members.list_members`<a id="launchdarklyaccount_memberslist_members"></a>

Return a list of account members.

By default, this returns the first 20 members. Page through this list with the `limit` parameter and by following the `first`, `prev`, `next`, and `last` links in the returned `_links` field. These links are not present if the pages they refer to don't exist. For example, the `first` and `prev` links will be missing from the response on the first page.

### Filtering members<a id="filtering-members"></a>

LaunchDarkly supports the following fields for filters:

- `query` is a string that matches against the members' emails and names. It is not case sensitive.
- `role` is a `|` separated list of roles and custom roles. It filters the list to members who have any of the roles in the list. For the purposes of this filtering, `Owner` counts as `Admin`.
- `team` is a string that matches against the key of the teams the members belong to. It is not case sensitive.
- `noteam` is a boolean that filters the list of members who are not on a team if true and members on a team if false.
- `lastSeen` is a JSON object in one of the following formats:
  - `{"never": true}` - Members that have never been active, such as those who have not accepted their invitation to LaunchDarkly, or have not logged in after being provisioned via SCIM.
  - `{"noData": true}` - Members that have not been active since LaunchDarkly began recording last seen timestamps.
  - `{"before": 1608672063611}` - Members that have not been active since the provided value, which should be a timestamp in Unix epoch milliseconds.
- `accessCheck` is a string that represents a specific action on a specific resource and is in the format `<ActionSpecifier>:<ResourceSpecifier>`. It filters the list to members who have the ability to perform that action on that resource. Note: `accessCheck` is only supported in API version `20220603` and earlier. To learn more, read [Versioning](https://apidocs.launchdarkly.com/#section/Overview/Versioning).
  - For example, the filter `accessCheck:createApprovalRequest:proj/default:env/test:flag/alternate-page` matches members with the ability to create an approval request for the `alternate-page` flag in the `test` environment of the `default` project.
  - Wildcard and tag filters are not supported when filtering for access.

For example, the filter `query:abc,role:admin|customrole` matches members with the string `abc` in their email or name, ignoring case, who also are either an `Owner` or `Admin` or have the custom role `customrole`.

### Sorting members<a id="sorting-members"></a>

LaunchDarkly supports two fields for sorting: `displayName` and `lastSeen`:

- `displayName` sorts by first + last name, using the member's email if no name is set.
- `lastSeen` sorts by the `_lastSeen` property. LaunchDarkly considers members that have never been seen or have no data the oldest.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_members_response = launchdarkly.account_members.list_members(
    limit=1,
    offset=1,
    filter="string_example",
    sort="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### limit: `int`<a id="limit-int"></a>

The number of members to return in the response. Defaults to 20.

##### offset: `int`<a id="offset-int"></a>

Where to start in the list. This is for use with pagination. For example, an offset of 10 skips the first ten items and then returns the next items in the list, up to the query `limit`.

##### filter: `str`<a id="filter-str"></a>

A comma-separated list of filters. Each filter is of the form `field:value`. Supported fields are explained above.

##### sort: `str`<a id="sort-str"></a>

A comma-separated list of fields to sort by. Fields prefixed by a dash ( - ) sort in descending order.

#### 🔄 Return<a id="🔄-return"></a>

[`Members`](./launch_darkly_python_sdk/pydantic/members.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/members` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.account_members.update_member_patch`<a id="launchdarklyaccount_membersupdate_member_patch"></a>


Update a single account member. Updating a member uses a [JSON patch](https://datatracker.ietf.org/doc/html/rfc6902) representation of the desired changes. To learn more, read [Updates](https://apidocs.launchdarkly.com).

To update fields in the account member object that are arrays, set the `path` to the name of the field and then append `/<array index>`. Use `/0` to add to the beginning of the array. Use `/-` to add to the end of the array. For example, to add a new custom role to a member, use the following request body:

```
  [
    {
      "op": "add",
      "path": "/customRoles/0",
      "value": "some-role-id"
    }
  ]
```

You can update only an account member's role or custom role using a JSON patch. Members can update their own names and email addresses though the LaunchDarkly UI.

When SAML SSO or SCIM is enabled for the account, account members are managed in the Identity Provider (IdP). Requests to update account members will succeed, but the IdP will override the update shortly afterwards.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
update_member_patch_response = launchdarkly.account_members.update_member_patch(
    body=[{"op":"add","path":"/role","value":"writer"}],
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

The member ID

##### requestBody: [`JSONPatch`](./launch_darkly_python_sdk/type/json_patch.py)<a id="requestbody-jsonpatchlaunch_darkly_python_sdktypejson_patchpy"></a>

#### 🔄 Return<a id="🔄-return"></a>

[`Member`](./launch_darkly_python_sdk/pydantic/member.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/members/{id}` `patch`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.account_members_(beta).modify_members_roles`<a id="launchdarklyaccount_members_betamodify_members_roles"></a>

> ### Full use of this API resource is an Enterprise feature
>
> The ability to perform a partial update to multiple members is available to customers on an Enterprise plan. If you are on a Pro plan, you can update members individually. To learn more, [read about our pricing](https://launchdarkly.com/pricing/). To upgrade your plan, [contact Sales](https://launchdarkly.com/contact-sales/).

Perform a partial update to multiple members. Updating members uses the semantic patch format.

To make a semantic patch request, you must append `domain-model=launchdarkly.semanticpatch` to your `Content-Type` header. To learn more, read [Updates using semantic patch](https://apidocs.launchdarkly.com).

### Instructions<a id="instructions"></a>

Semantic patch requests support the following `kind` instructions for updating members.

<details>
<summary>Click to expand instructions for <strong>updating members</strong></summary>

#### replaceMembersRoles<a id="replacemembersroles"></a>

Replaces the roles of the specified members. This also removes all custom roles assigned to the specified members.

##### Parameters<a id="parameters"></a>

- `value`: The new role. Must be a valid built-in role. To learn more about built-in roles, read [LaunchDarkly's built-in roles](https://docs.launchdarkly.com/home/members/built-in-roles).
- `memberIDs`: List of member IDs.

Here's an example:

```json
{
  "instructions": [{
    "kind": "replaceMemberRoles",
    "value": "reader",
    "memberIDs": [
      "1234a56b7c89d012345e678f",
      "507f1f77bcf86cd799439011"
    ]
  }]
}
```

#### replaceAllMembersRoles<a id="replaceallmembersroles"></a>

Replaces the roles of all members. This also removes all custom roles assigned to the specified members.

Members that match any of the filters are **excluded** from the update.

##### Parameters<a id="parameters"></a>

- `value`: The new role. Must be a valid built-in role. To learn more about built-in roles, read [LaunchDarkly's built-in roles](https://docs.launchdarkly.com/home/members/built-in-roles).
- `filterLastSeen`: (Optional) A JSON object with one of the following formats:
  - `{"never": true}` - Members that have never been active, such as those who have not accepted their invitation to LaunchDarkly, or have not logged in after being provisioned via SCIM.
  - `{"noData": true}` - Members that have not been active since LaunchDarkly began recording last seen timestamps.
  - `{"before": 1608672063611}` - Members that have not been active since the provided value, which should be a timestamp in Unix epoch milliseconds.
- `filterQuery`: (Optional) A string that matches against the members' emails and names. It is not case sensitive.
- `filterRoles`: (Optional) A `|` separated list of roles and custom roles. For the purposes of this filtering, `Owner` counts as `Admin`.
- `filterTeamKey`: (Optional) A string that matches against the key of the team the members belong to. It is not case sensitive.
- `ignoredMemberIDs`: (Optional) A list of member IDs.

Here's an example:

```json
{
  "instructions": [{
    "kind": "replaceAllMembersRoles",
    "value": "reader",
    "filterLastSeen": { "never": true }
  }]
}
```

#### replaceMembersCustomRoles<a id="replacememberscustomroles"></a>

Replaces the custom roles of the specified members.

##### Parameters<a id="parameters"></a>

- `values`: List of new custom roles. Must be a valid custom role key or ID.
- `memberIDs`: List of member IDs.

Here's an example:

```json
{
  "instructions": [{
    "kind": "replaceMembersCustomRoles",
    "values": [ "example-custom-role" ],
    "memberIDs": [
      "1234a56b7c89d012345e678f",
      "507f1f77bcf86cd799439011"
    ]
  }]
}
```

#### replaceAllMembersCustomRoles<a id="replaceallmemberscustomroles"></a>

Replaces the custom roles of all members. Members that match any of the filters are **excluded** from the update.

##### Parameters<a id="parameters"></a>

- `values`: List of new roles. Must be a valid custom role key or ID.
- `filterLastSeen`: (Optional) A JSON object with one of the following formats:
  - `{"never": true}` - Members that have never been active, such as those who have not accepted their invitation to LaunchDarkly, or have not logged in after being provisioned via SCIM.
  - `{"noData": true}` - Members that have not been active since LaunchDarkly began recording last seen timestamps.
  - `{"before": 1608672063611}` - Members that have not been active since the provided value, which should be a timestamp in Unix epoch milliseconds.
- `filterQuery`: (Optional) A string that matches against the members' emails and names. It is not case sensitive.
- `filterRoles`: (Optional) A `|` separated list of roles and custom roles. For the purposes of this filtering, `Owner` counts as `Admin`.
- `filterTeamKey`: (Optional) A string that matches against the key of the team the members belong to. It is not case sensitive.
- `ignoredMemberIDs`: (Optional) A list of member IDs.

Here's an example:

```json
{
  "instructions": [{
    "kind": "replaceAllMembersCustomRoles",
    "values": [ "example-custom-role" ],
    "filterLastSeen": { "never": true }
  }]
}
```

</details>


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
modify_members_roles_response = launchdarkly.account_members_(beta).modify_members_roles(
    instructions=[
        {
            "key": None,
        }
    ],
    comment="Optional comment about the update",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### instructions: [`Instructions`](./launch_darkly_python_sdk/type/instructions.py)<a id="instructions-instructionslaunch_darkly_python_sdktypeinstructionspy"></a>

##### comment: `str`<a id="comment-str"></a>

Optional comment describing the update

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`MembersPatchInput`](./launch_darkly_python_sdk/type/members_patch_input.py)
#### 🔄 Return<a id="🔄-return"></a>

[`BulkEditMembersRep`](./launch_darkly_python_sdk/pydantic/bulk_edit_members_rep.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/members` `patch`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.account_usage_(beta).get_evaluations_usage`<a id="launchdarklyaccount_usage_betaget_evaluations_usage"></a>

Get time-series arrays of the number of times a flag is evaluated, broken down by the variation that resulted from that evaluation. The granularity of the data depends on the age of the data requested. If the requested range is within the past two hours, minutely data is returned. If it is within the last two days, hourly data is returned. Otherwise, daily data is returned.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_evaluations_usage_response = launchdarkly.account_usage_(beta).get_evaluations_usage(
    project_key="projectKey_example",
    environment_key="environmentKey_example",
    feature_flag_key="featureFlagKey_example",
    _from="string_example",
    to="string_example",
    tz="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

##### feature_flag_key: `str`<a id="feature_flag_key-str"></a>

The feature flag key

##### _from: `str`<a id="_from-str"></a>

The series of data returned starts from this timestamp. Defaults to 30 days ago.

##### to: `str`<a id="to-str"></a>

The series of data returned ends at this timestamp. Defaults to the current time.

##### tz: `str`<a id="tz-str"></a>

The timezone to use for breaks between days when returning daily data.

#### 🔄 Return<a id="🔄-return"></a>

[`SeriesListRep`](./launch_darkly_python_sdk/pydantic/series_list_rep.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/usage/evaluations/{projectKey}/{environmentKey}/{featureFlagKey}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.account_usage_(beta).get_events_usage_data`<a id="launchdarklyaccount_usage_betaget_events_usage_data"></a>

Get time-series arrays of the number of times a flag is evaluated, broken down by the variation that resulted from that evaluation. The granularity of the data depends on the age of the data requested. If the requested range is within the past two hours, minutely data is returned. If it is within the last two days, hourly data is returned. Otherwise, daily data is returned.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_events_usage_data_response = launchdarkly.account_usage_(beta).get_events_usage_data(
    type="type_example",
    _from="string_example",
    to="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### type: `str`<a id="type-str"></a>

The type of event to retrieve. Must be either `received` or `published`.

##### _from: `str`<a id="_from-str"></a>

The series of data returned starts from this timestamp. Defaults to 24 hours ago.

##### to: `str`<a id="to-str"></a>

The series of data returned ends at this timestamp. Defaults to the current time.

#### 🔄 Return<a id="🔄-return"></a>

[`SeriesListRep`](./launch_darkly_python_sdk/pydantic/series_list_rep.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/usage/events/{type}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.account_usage_(beta).get_experimentation_keys_usage`<a id="launchdarklyaccount_usage_betaget_experimentation_keys_usage"></a>

Get a time-series array of the number of monthly experimentation keys from your account. The granularity is always daily, with a maximum of 31 days.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_experimentation_keys_usage_response = launchdarkly.account_usage_(beta).get_experimentation_keys_usage(
    _from="string_example",
    to="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### _from: `str`<a id="_from-str"></a>

The series of data returned starts from this timestamp (Unix seconds). Defaults to the beginning of the current month.

##### to: `str`<a id="to-str"></a>

The series of data returned ends at this timestamp (Unix seconds). Defaults to the current time.

#### 🔄 Return<a id="🔄-return"></a>

[`SeriesIntervalsRep`](./launch_darkly_python_sdk/pydantic/series_intervals_rep.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/usage/experimentation-keys` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.account_usage_(beta).get_experimentation_units_usage`<a id="launchdarklyaccount_usage_betaget_experimentation_units_usage"></a>

Get a time-series array of the number of monthly experimentation units from your account. The granularity is always daily, with a maximum of 31 days.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_experimentation_units_usage_response = launchdarkly.account_usage_(beta).get_experimentation_units_usage(
    _from="string_example",
    to="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### _from: `str`<a id="_from-str"></a>

The series of data returned starts from this timestamp (Unix seconds). Defaults to the beginning of the current month.

##### to: `str`<a id="to-str"></a>

The series of data returned ends at this timestamp (Unix seconds). Defaults to the current time.

#### 🔄 Return<a id="🔄-return"></a>

[`SeriesIntervalsRep`](./launch_darkly_python_sdk/pydantic/series_intervals_rep.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/usage/experimentation-units` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.account_usage_(beta).get_mau_usage_by_category`<a id="launchdarklyaccount_usage_betaget_mau_usage_by_category"></a>

Get time-series arrays of the number of monthly active users (MAU) seen by LaunchDarkly from your account, broken down by the category of users. The category is either `browser`, `mobile`, or `backend`.<br/><br/>Endpoints for retrieving monthly active users (MAU) do not return information about active context instances. After you have upgraded your LaunchDarkly SDK to use contexts instead of users, you should not rely on this endpoint. To learn more, read [Account usage metrics](https://docs.launchdarkly.com/home/billing/usage-metrics).

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_mau_usage_by_category_response = launchdarkly.account_usage_(beta).get_mau_usage_by_category(
    _from="string_example",
    to="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### _from: `str`<a id="_from-str"></a>

The series of data returned starts from this timestamp. Defaults to 30 days ago.

##### to: `str`<a id="to-str"></a>

The series of data returned ends at this timestamp. Defaults to the current time.

#### 🔄 Return<a id="🔄-return"></a>

[`SeriesListRep`](./launch_darkly_python_sdk/pydantic/series_list_rep.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/usage/mau/bycategory` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.account_usage_(beta).get_mau_usage_data`<a id="launchdarklyaccount_usage_betaget_mau_usage_data"></a>

Get a time-series array of the number of monthly active users (MAU) seen by LaunchDarkly from your account. The granularity is always daily.<br/><br/>Endpoints for retrieving monthly active users (MAU) do not return information about active context instances. After you have upgraded your LaunchDarkly SDK to use contexts instead of users, you should not rely on this endpoint. To learn more, read [Account usage metrics](https://docs.launchdarkly.com/home/billing/usage-metrics).

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_mau_usage_data_response = launchdarkly.account_usage_(beta).get_mau_usage_data(
    _from="string_example",
    to="string_example",
    project="string_example",
    environment="string_example",
    sdktype="string_example",
    sdk="string_example",
    anonymous="string_example",
    groupby="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### _from: `str`<a id="_from-str"></a>

The series of data returned starts from this timestamp. Defaults to 30 days ago.

##### to: `str`<a id="to-str"></a>

The series of data returned ends at this timestamp. Defaults to the current time.

##### project: `str`<a id="project-str"></a>

A project key to filter results to. Can be specified multiple times, one query parameter per project key, to view data for multiple projects.

##### environment: `str`<a id="environment-str"></a>

An environment key to filter results to. When using this parameter, exactly one project key must also be set. Can be specified multiple times as separate query parameters to view data for multiple environments within a single project.

##### sdktype: `str`<a id="sdktype-str"></a>

An SDK type to filter results to. Can be specified multiple times, one query parameter per SDK type. Valid values: client, server

##### sdk: `str`<a id="sdk-str"></a>

An SDK name to filter results to. Can be specified multiple times, one query parameter per SDK.

##### anonymous: `str`<a id="anonymous-str"></a>

If specified, filters results to either anonymous or nonanonymous users.

##### groupby: `str`<a id="groupby-str"></a>

If specified, returns data for each distinct value of the given field. Can be specified multiple times to group data by multiple dimensions (for example, to group by both project and SDK). Valid values: project, environment, sdktype, sdk, anonymous

#### 🔄 Return<a id="🔄-return"></a>

[`SeriesListRep`](./launch_darkly_python_sdk/pydantic/series_list_rep.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/usage/mau` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.account_usage_(beta).get_stream_usage`<a id="launchdarklyaccount_usage_betaget_stream_usage"></a>

Get a time-series array of the number of streaming connections to LaunchDarkly in each time period. The granularity of the data depends on the age of the data requested. If the requested range is within the past two hours, minutely data is returned. If it is within the last two days, hourly data is returned. Otherwise, daily data is returned.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_stream_usage_response = launchdarkly.account_usage_(beta).get_stream_usage(
    source="source_example",
    _from="string_example",
    to="string_example",
    tz="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### source: `str`<a id="source-str"></a>

The source of streaming connections to describe. Must be either `client` or `server`.

##### _from: `str`<a id="_from-str"></a>

The series of data returned starts from this timestamp. Defaults to 30 days ago.

##### to: `str`<a id="to-str"></a>

The series of data returned ends at this timestamp. Defaults to the current time.

##### tz: `str`<a id="tz-str"></a>

The timezone to use for breaks between days when returning daily data.

#### 🔄 Return<a id="🔄-return"></a>

[`SeriesListRep`](./launch_darkly_python_sdk/pydantic/series_list_rep.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/usage/streams/{source}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.account_usage_(beta).get_stream_usage_by_sdk_version_data`<a id="launchdarklyaccount_usage_betaget_stream_usage_by_sdk_version_data"></a>

Get multiple series of the number of streaming connections to LaunchDarkly in each time period, separated by SDK type and version. Information about each series is in the metadata array. The granularity of the data depends on the age of the data requested. If the requested range is within the past 2 hours, minutely data is returned. If it is within the last two days, hourly data is returned. Otherwise, daily data is returned.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_stream_usage_by_sdk_version_data_response = launchdarkly.account_usage_(beta).get_stream_usage_by_sdk_version_data(
    source="source_example",
    _from="string_example",
    to="string_example",
    tz="string_example",
    sdk="string_example",
    version="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### source: `str`<a id="source-str"></a>

The source of streaming connections to describe. Must be either `client` or `server`.

##### _from: `str`<a id="_from-str"></a>

The series of data returned starts from this timestamp. Defaults to 24 hours ago.

##### to: `str`<a id="to-str"></a>

The series of data returned ends at this timestamp. Defaults to the current time.

##### tz: `str`<a id="tz-str"></a>

The timezone to use for breaks between days when returning daily data.

##### sdk: `str`<a id="sdk-str"></a>

If included, this filters the returned series to only those that match this SDK name.

##### version: `str`<a id="version-str"></a>

If included, this filters the returned series to only those that match this SDK version.

#### 🔄 Return<a id="🔄-return"></a>

[`SeriesListRep`](./launch_darkly_python_sdk/pydantic/series_list_rep.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/usage/streams/{source}/bysdkversion` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.account_usage_(beta).list_mau_sdks_by_type`<a id="launchdarklyaccount_usage_betalist_mau_sdks_by_type"></a>

Get a list of SDKs. These are all of the SDKs that have connected to LaunchDarkly by monthly active users (MAU) in the requested time period.<br/><br/>Endpoints for retrieving monthly active users (MAU) do not return information about active context instances. After you have upgraded your LaunchDarkly SDK to use contexts instead of users, you should not rely on this endpoint. To learn more, read [Account usage metrics](https://docs.launchdarkly.com/home/billing/usage-metrics).

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_mau_sdks_by_type_response = launchdarkly.account_usage_(beta).list_mau_sdks_by_type(
    _from="string_example",
    to="string_example",
    sdktype="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### _from: `str`<a id="_from-str"></a>

The data returned starts from this timestamp. Defaults to seven days ago. The timestamp is in Unix milliseconds, for example, 1656694800000.

##### to: `str`<a id="to-str"></a>

The data returned ends at this timestamp. Defaults to the current time. The timestamp is in Unix milliseconds, for example, 1657904400000.

##### sdktype: `str`<a id="sdktype-str"></a>

The type of SDK with monthly active users (MAU) to list. Must be either `client` or `server`.

#### 🔄 Return<a id="🔄-return"></a>

[`SdkListRep`](./launch_darkly_python_sdk/pydantic/sdk_list_rep.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/usage/mau/sdks` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.account_usage_(beta).list_sdk_versions`<a id="launchdarklyaccount_usage_betalist_sdk_versions"></a>

Get a list of SDK version objects, which contain an SDK name and version. These are all of the SDKs that have connected to LaunchDarkly from your account in the past 60 days.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_sdk_versions_response = launchdarkly.account_usage_(beta).list_sdk_versions(
    source="source_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### source: `str`<a id="source-str"></a>

The source of streaming connections to describe. Must be either `client` or `server`.

#### 🔄 Return<a id="🔄-return"></a>

[`SdkVersionListRep`](./launch_darkly_python_sdk/pydantic/sdk_version_list_rep.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/usage/streams/{source}/sdkversions` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.applications_(beta).get_application_by_key`<a id="launchdarklyapplications_betaget_application_by_key"></a>


Retrieve an application by the application key.

### Expanding the application response<a id="expanding-the-application-response"></a>

LaunchDarkly supports expanding the "Get application" response to include additional fields.

To expand the response, append the `expand` query parameter and include the following:

* `flags` includes details on the flags that have been evaluated by the application

For example, use `?expand=flags` to include the `flags` field in the response. By default, this field is **not** included in the response.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_application_by_key_response = launchdarkly.applications_(beta).get_application_by_key(
    application_key="applicationKey_example",
    expand="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### application_key: `str`<a id="application_key-str"></a>

The application key

##### expand: `str`<a id="expand-str"></a>

A comma-separated list of properties that can reveal additional information in the response. Options: `flags`.

#### 🔄 Return<a id="🔄-return"></a>

[`ApplicationRep`](./launch_darkly_python_sdk/pydantic/application_rep.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/applications/{applicationKey}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.applications_(beta).get_application_versions`<a id="launchdarklyapplications_betaget_application_versions"></a>

Get a list of versions for a specific application in an account.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_application_versions_response = launchdarkly.applications_(beta).get_application_versions(
    application_key="applicationKey_example",
    filter="string_example",
    limit=1,
    offset=1,
    sort="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### application_key: `str`<a id="application_key-str"></a>

The application key

##### filter: `str`<a id="filter-str"></a>

Accepts filter by `key`, `name`, `supported`, and `autoAdded`. Example: `filter=key equals 'test-key'`. To learn more about the filter syntax, read [Filtering applications and application versions](https://apidocs.launchdarkly.com)#filtering-contexts-and-context-instances).

##### limit: `int`<a id="limit-int"></a>

The number of versions to return. Defaults to 50.

##### offset: `int`<a id="offset-int"></a>

Where to start in the list. Use this with pagination. For example, an offset of 10 skips the first ten items and then returns the next items in the list, up to the query `limit`.

##### sort: `str`<a id="sort-str"></a>

Accepts sorting order and fields. Fields can be comma separated. Possible fields are `creationDate`, `name`. Examples: `sort=name` sort by names ascending, `sort=-name,creationDate` sort by names descending and creationDate ascending.

#### 🔄 Return<a id="🔄-return"></a>

[`ApplicationVersionsCollectionRep`](./launch_darkly_python_sdk/pydantic/application_versions_collection_rep.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/applications/{applicationKey}/versions` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.applications_(beta).list_applications`<a id="launchdarklyapplications_betalist_applications"></a>


Get a list of applications.

### Expanding the applications response<a id="expanding-the-applications-response"></a>

LaunchDarkly supports expanding the "Get applications" response to include additional fields.

To expand the response, append the `expand` query parameter and include the following:

* `flags` includes details on the flags that have been evaluated by the application

For example, use `?expand=flags` to include the `flags` field in the response. By default, this field is **not** included in the response.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_applications_response = launchdarkly.applications_(beta).list_applications(
    filter="string_example",
    limit=1,
    offset=1,
    sort="string_example",
    expand="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### filter: `str`<a id="filter-str"></a>

Accepts filter by `key`, `name`, `kind`, and `autoAdded`. Example: `filter=kind anyOf ['mobile', 'server'],key equals 'test-key'`. To learn more about the filter syntax, read [Filtering applications and application versions](https://apidocs.launchdarkly.com)#filtering-contexts-and-context-instances).

##### limit: `int`<a id="limit-int"></a>

The number of applications to return. Defaults to 10.

##### offset: `int`<a id="offset-int"></a>

Where to start in the list. Use this with pagination. For example, an offset of 10 skips the first ten items and then returns the next items in the list, up to the query `limit`.

##### sort: `str`<a id="sort-str"></a>

Accepts sorting order and fields. Fields can be comma separated. Possible fields are `creationDate`, `name`. Examples: `sort=name` sort by names ascending, `sort=-name,creationDate` sort by names descending and creationDate ascending.

##### expand: `str`<a id="expand-str"></a>

A comma-separated list of properties that can reveal additional information in the response. Options: `flags`.

#### 🔄 Return<a id="🔄-return"></a>

[`ApplicationCollectionRep`](./launch_darkly_python_sdk/pydantic/application_collection_rep.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/applications` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.applications_(beta).remove_application`<a id="launchdarklyapplications_betaremove_application"></a>

Delete an application.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
launchdarkly.applications_(beta).remove_application(
    application_key="applicationKey_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### application_key: `str`<a id="application_key-str"></a>

The application key

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/applications/{applicationKey}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.applications_(beta).remove_version`<a id="launchdarklyapplications_betaremove_version"></a>

Delete an application version.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
launchdarkly.applications_(beta).remove_version(
    application_key="applicationKey_example",
    version_key="versionKey_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### application_key: `str`<a id="application_key-str"></a>

The application key

##### version_key: `str`<a id="version_key-str"></a>

The application version key

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/applications/{applicationKey}/versions/{versionKey}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.applications_(beta).update_application_patch`<a id="launchdarklyapplications_betaupdate_application_patch"></a>

Update an application. You can update the `description` and `kind` fields. Requires a [JSON patch](https://datatracker.ietf.org/doc/html/rfc6902) representation of the desired changes to the application. To learn more, read [Updates](https://apidocs.launchdarkly.com).

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
update_application_patch_response = launchdarkly.applications_(beta).update_application_patch(
    body=[{"op":"replace","path":"/description","value":"Updated description"}],
    application_key="applicationKey_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### application_key: `str`<a id="application_key-str"></a>

The application key

##### requestBody: [`JSONPatch`](./launch_darkly_python_sdk/type/json_patch.py)<a id="requestbody-jsonpatchlaunch_darkly_python_sdktypejson_patchpy"></a>

#### 🔄 Return<a id="🔄-return"></a>

[`ApplicationRep`](./launch_darkly_python_sdk/pydantic/application_rep.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/applications/{applicationKey}` `patch`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.applications_(beta).update_version_patch`<a id="launchdarklyapplications_betaupdate_version_patch"></a>

Update an application version. You can update the `supported` field. Requires a [JSON patch](https://datatracker.ietf.org/doc/html/rfc6902) representation of the desired changes to the application version. To learn more, read [Updates](https://apidocs.launchdarkly.com).

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
update_version_patch_response = launchdarkly.applications_(beta).update_version_patch(
    body=[{"op":"replace","path":"/supported","value":"false"}],
    application_key="applicationKey_example",
    version_key="versionKey_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### application_key: `str`<a id="application_key-str"></a>

The application key

##### version_key: `str`<a id="version_key-str"></a>

The application version key

##### requestBody: [`JSONPatch`](./launch_darkly_python_sdk/type/json_patch.py)<a id="requestbody-jsonpatchlaunch_darkly_python_sdktypejson_patchpy"></a>

#### 🔄 Return<a id="🔄-return"></a>

[`ApplicationVersionRep`](./launch_darkly_python_sdk/pydantic/application_version_rep.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/applications/{applicationKey}/versions/{versionKey}` `patch`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.approvals.apply_request_flag`<a id="launchdarklyapprovalsapply_request_flag"></a>

Apply an approval request that has been approved.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
apply_request_flag_response = launchdarkly.approvals.apply_request_flag(
    id="id_example",
    comment="Looks good, thanks for updating",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

The feature flag approval request ID

##### comment: `str`<a id="comment-str"></a>

Optional comment about the approval request

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`PostApprovalRequestApplyRequest`](./launch_darkly_python_sdk/type/post_approval_request_apply_request.py)
#### 🔄 Return<a id="🔄-return"></a>

[`ApprovalRequestResponse`](./launch_darkly_python_sdk/pydantic/approval_request_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/approval-requests/{id}/apply` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.approvals.apply_request_flag_0`<a id="launchdarklyapprovalsapply_request_flag_0"></a>

Apply an approval request that has been approved.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
apply_request_flag_0_response = launchdarkly.approvals.apply_request_flag_0(
    project_key="projectKey_example",
    feature_flag_key="featureFlagKey_example",
    environment_key="environmentKey_example",
    id="id_example",
    comment="Looks good, thanks for updating",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### feature_flag_key: `str`<a id="feature_flag_key-str"></a>

The feature flag key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

##### id: `str`<a id="id-str"></a>

The feature flag approval request ID

##### comment: `str`<a id="comment-str"></a>

Optional comment about the approval request

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`PostApprovalRequestApplyRequest`](./launch_darkly_python_sdk/type/post_approval_request_apply_request.py)
#### 🔄 Return<a id="🔄-return"></a>

[`FlagConfigApprovalRequestResponse`](./launch_darkly_python_sdk/pydantic/flag_config_approval_request_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/projects/{projectKey}/flags/{featureFlagKey}/environments/{environmentKey}/approval-requests/{id}/apply` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.approvals.create_flag_copy_request`<a id="launchdarklyapprovalscreate_flag_copy_request"></a>

Create an approval request to copy a feature flag's configuration across environments.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
create_flag_copy_request_response = launchdarkly.approvals.create_flag_copy_request(
    description="copy flag settings to another environment",
    source={
        "version": 1,
        "key": "environment-key-123abc",
    },
    project_key="projectKey_example",
    feature_flag_key="featureFlagKey_example",
    environment_key="environmentKey_example",
    comment="optional comment",
    notify_member_ids=["1234a56b7c89d012345e678f"],
    notify_team_keys=["example-reviewer-team"],
    included_actions=["updateOn"],
    excluded_actions=["updateOn"],
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### description: `str`<a id="description-str"></a>

A brief description of your changes

##### source: [`SourceFlag`](./launch_darkly_python_sdk/type/source_flag.py)<a id="source-sourceflaglaunch_darkly_python_sdktypesource_flagpy"></a>


##### project_key: `str`<a id="project_key-str"></a>

The project key

##### feature_flag_key: `str`<a id="feature_flag_key-str"></a>

The feature flag key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key for the target environment

##### comment: `str`<a id="comment-str"></a>

Optional comment describing the approval request

##### notify_member_ids: [`CreateCopyFlagConfigApprovalRequestRequestNotifyMemberIds`](./launch_darkly_python_sdk/type/create_copy_flag_config_approval_request_request_notify_member_ids.py)<a id="notify_member_ids-createcopyflagconfigapprovalrequestrequestnotifymemberidslaunch_darkly_python_sdktypecreate_copy_flag_config_approval_request_request_notify_member_idspy"></a>

##### notify_team_keys: [`CreateCopyFlagConfigApprovalRequestRequestNotifyTeamKeys`](./launch_darkly_python_sdk/type/create_copy_flag_config_approval_request_request_notify_team_keys.py)<a id="notify_team_keys-createcopyflagconfigapprovalrequestrequestnotifyteamkeyslaunch_darkly_python_sdktypecreate_copy_flag_config_approval_request_request_notify_team_keyspy"></a>

##### included_actions: [`CreateCopyFlagConfigApprovalRequestRequestIncludedActions`](./launch_darkly_python_sdk/type/create_copy_flag_config_approval_request_request_included_actions.py)<a id="included_actions-createcopyflagconfigapprovalrequestrequestincludedactionslaunch_darkly_python_sdktypecreate_copy_flag_config_approval_request_request_included_actionspy"></a>

##### excluded_actions: [`CreateCopyFlagConfigApprovalRequestRequestExcludedActions`](./launch_darkly_python_sdk/type/create_copy_flag_config_approval_request_request_excluded_actions.py)<a id="excluded_actions-createcopyflagconfigapprovalrequestrequestexcludedactionslaunch_darkly_python_sdktypecreate_copy_flag_config_approval_request_request_excluded_actionspy"></a>

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`CreateCopyFlagConfigApprovalRequestRequest`](./launch_darkly_python_sdk/type/create_copy_flag_config_approval_request_request.py)
#### 🔄 Return<a id="🔄-return"></a>

[`FlagConfigApprovalRequestResponse`](./launch_darkly_python_sdk/pydantic/flag_config_approval_request_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/projects/{projectKey}/flags/{featureFlagKey}/environments/{environmentKey}/approval-requests-flag-copy` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.approvals.create_request_flag`<a id="launchdarklyapprovalscreate_request_flag"></a>

Create an approval request.

This endpoint currently supports creating an approval request for a flag across all environments with the following instructions:

- `addVariation`
- `removeVariation`
- `updateVariation`
- `updateDefaultVariation`

For details on using these instructions, read [Update feature flag](https://apidocs.launchdarkly.com).

To create an approval for a flag specific to an environment, use [Create approval request for a flag](https://apidocs.launchdarkly.com).


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
create_request_flag_response = launchdarkly.approvals.create_request_flag(
    description="Requesting to update targeting",
    resource_id="string_example",
    instructions=[
        {
            "key": None,
        }
    ],
    comment="optional comment",
    notify_member_ids=["1234a56b7c89d012345e678f"],
    notify_team_keys=["example-reviewer-team"],
    integration_config={
        "key": None,
    },
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### description: `str`<a id="description-str"></a>

A brief description of the changes you're requesting

##### resource_id: `str`<a id="resource_id-str"></a>

String representation of a resource

##### instructions: [`Instructions`](./launch_darkly_python_sdk/type/instructions.py)<a id="instructions-instructionslaunch_darkly_python_sdktypeinstructionspy"></a>

##### comment: `str`<a id="comment-str"></a>

Optional comment describing the approval request

##### notify_member_ids: [`CreateApprovalRequestRequestNotifyMemberIds`](./launch_darkly_python_sdk/type/create_approval_request_request_notify_member_ids.py)<a id="notify_member_ids-createapprovalrequestrequestnotifymemberidslaunch_darkly_python_sdktypecreate_approval_request_request_notify_member_idspy"></a>

##### notify_team_keys: [`CreateApprovalRequestRequestNotifyTeamKeys`](./launch_darkly_python_sdk/type/create_approval_request_request_notify_team_keys.py)<a id="notify_team_keys-createapprovalrequestrequestnotifyteamkeyslaunch_darkly_python_sdktypecreate_approval_request_request_notify_team_keyspy"></a>

##### integration_config: [`FormVariableConfig`](./launch_darkly_python_sdk/type/form_variable_config.py)<a id="integration_config-formvariableconfiglaunch_darkly_python_sdktypeform_variable_configpy"></a>

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`CreateApprovalRequestRequest`](./launch_darkly_python_sdk/type/create_approval_request_request.py)
#### 🔄 Return<a id="🔄-return"></a>

[`ApprovalRequestResponse`](./launch_darkly_python_sdk/pydantic/approval_request_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/approval-requests` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.approvals.create_request_flag_0`<a id="launchdarklyapprovalscreate_request_flag_0"></a>

Create an approval request for a feature flag.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
create_request_flag_0_response = launchdarkly.approvals.create_request_flag_0(
    description="Requesting to update targeting",
    instructions=[
        {
            "key": None,
        }
    ],
    project_key="projectKey_example",
    feature_flag_key="featureFlagKey_example",
    environment_key="environmentKey_example",
    comment="optional comment",
    notify_member_ids=["1234a56b7c89d012345e678f"],
    notify_team_keys=["example-reviewer-team"],
    execution_date=1,
    operating_on_id="6297ed79dee7dc14e1f9a80c",
    integration_config={
        "key": None,
    },
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### description: `str`<a id="description-str"></a>

A brief description of the changes you're requesting

##### instructions: [`Instructions`](./launch_darkly_python_sdk/type/instructions.py)<a id="instructions-instructionslaunch_darkly_python_sdktypeinstructionspy"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### feature_flag_key: `str`<a id="feature_flag_key-str"></a>

The feature flag key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

##### comment: `str`<a id="comment-str"></a>

Optional comment describing the approval request

##### notify_member_ids: [`CreateFlagConfigApprovalRequestRequestNotifyMemberIds`](./launch_darkly_python_sdk/type/create_flag_config_approval_request_request_notify_member_ids.py)<a id="notify_member_ids-createflagconfigapprovalrequestrequestnotifymemberidslaunch_darkly_python_sdktypecreate_flag_config_approval_request_request_notify_member_idspy"></a>

##### notify_team_keys: [`CreateFlagConfigApprovalRequestRequestNotifyTeamKeys`](./launch_darkly_python_sdk/type/create_flag_config_approval_request_request_notify_team_keys.py)<a id="notify_team_keys-createflagconfigapprovalrequestrequestnotifyteamkeyslaunch_darkly_python_sdktypecreate_flag_config_approval_request_request_notify_team_keyspy"></a>

##### execution_date: `int`<a id="execution_date-int"></a>

##### operating_on_id: `str`<a id="operating_on_id-str"></a>

The ID of a scheduled change. Include this if your <code>instructions</code> include editing or deleting a scheduled change.

##### integration_config: [`FormVariableConfig`](./launch_darkly_python_sdk/type/form_variable_config.py)<a id="integration_config-formvariableconfiglaunch_darkly_python_sdktypeform_variable_configpy"></a>

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`CreateFlagConfigApprovalRequestRequest`](./launch_darkly_python_sdk/type/create_flag_config_approval_request_request.py)
#### 🔄 Return<a id="🔄-return"></a>

[`FlagConfigApprovalRequestResponse`](./launch_darkly_python_sdk/pydantic/flag_config_approval_request_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/projects/{projectKey}/flags/{featureFlagKey}/environments/{environmentKey}/approval-requests` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.approvals.delete_approval_request_flag`<a id="launchdarklyapprovalsdelete_approval_request_flag"></a>

Delete an approval request for a feature flag.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
launchdarkly.approvals.delete_approval_request_flag(
    project_key="projectKey_example",
    feature_flag_key="featureFlagKey_example",
    environment_key="environmentKey_example",
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### feature_flag_key: `str`<a id="feature_flag_key-str"></a>

The feature flag key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

##### id: `str`<a id="id-str"></a>

The feature flag approval request ID

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/projects/{projectKey}/flags/{featureFlagKey}/environments/{environmentKey}/approval-requests/{id}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.approvals.delete_request`<a id="launchdarklyapprovalsdelete_request"></a>

Delete an approval request.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
launchdarkly.approvals.delete_request(
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

The approval request ID

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/approval-requests/{id}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.approvals.get_request_by_id`<a id="launchdarklyapprovalsget_request_by_id"></a>

Get an approval request by approval request ID.

### Expanding approval response<a id="expanding-approval-response"></a>

LaunchDarkly supports the `expand` query param to include additional fields in the response, with the following fields:

- `flag` includes the flag the approval request belongs to
- `project` includes the project the approval request belongs to
- `environments` includes the environments the approval request relates to

For example, `expand=project,flag` includes the `project` and `flag` fields in the response.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_request_by_id_response = launchdarkly.approvals.get_request_by_id(
    id="id_example",
    expand="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

The approval request ID

##### expand: `str`<a id="expand-str"></a>

A comma-separated list of fields to expand in the response. Supported fields are explained above.

#### 🔄 Return<a id="🔄-return"></a>

[`ExpandableApprovalRequestResponse`](./launch_darkly_python_sdk/pydantic/expandable_approval_request_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/approval-requests/{id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.approvals.list`<a id="launchdarklyapprovalslist"></a>

Get all approval requests.

### Filtering approvals<a id="filtering-approvals"></a>

LaunchDarkly supports the `filter` query param for filtering, with the following fields:

- `notifyMemberIds` filters for only approvals that are assigned to a member in the specified list. For example: `filter=notifyMemberIds anyOf ["memberId1", "memberId2"]`.
- `requestorId` filters for only approvals that correspond to the ID of the member who requested the approval. For example: `filter=requestorId equals 457034721476302714390214`.
- `resourceId` filters for only approvals that correspond to the the specified resource identifier. For example: `filter=resourceId equals proj/my-project:env/my-environment:flag/my-flag`.
- `reviewStatus` filters for only approvals which correspond to the review status in the specified list. The possible values are `approved`, `declined`, and `pending`. For example: `filter=reviewStatus anyOf ["pending", "approved"]`.
- `status` filters for only approvals which correspond to the status in the specified list. The possible values are `pending`, `scheduled`, `failed`, and `completed`. For example: `filter=status anyOf ["pending", "scheduled"]`.

You can also apply multiple filters at once. For example, setting `filter=projectKey equals my-project, reviewStatus anyOf ["pending","approved"]` matches approval requests which correspond to the `my-project` project key, and a review status of either `pending` or `approved`.

### Expanding approval response<a id="expanding-approval-response"></a>

LaunchDarkly supports the `expand` query param to include additional fields in the response, with the following fields:

- `flag` includes the flag the approval request belongs to
- `project` includes the project the approval request belongs to
- `environments` includes the environments the approval request relates to

For example, `expand=project,flag` includes the `project` and `flag` fields in the response.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_response = launchdarkly.approvals.list(
    filter="string_example",
    expand="string_example",
    limit=1,
    offset=1,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### filter: `str`<a id="filter-str"></a>

A comma-separated list of filters. Each filter is of the form `field operator value`. Supported fields are explained above.

##### expand: `str`<a id="expand-str"></a>

A comma-separated list of fields to expand in the response. Supported fields are explained above.

##### limit: `int`<a id="limit-int"></a>

The number of approvals to return. Defaults to 20. Maximum limit is 200.

##### offset: `int`<a id="offset-int"></a>

Where to start in the list. Use this with pagination. For example, an offset of 10 skips the first ten items and then returns the next items in the list, up to the query `limit`.

#### 🔄 Return<a id="🔄-return"></a>

[`ExpandableApprovalRequestsResponse`](./launch_darkly_python_sdk/pydantic/expandable_approval_requests_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/approval-requests` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.approvals.list_requests_for_flag`<a id="launchdarklyapprovalslist_requests_for_flag"></a>

Get all approval requests for a feature flag.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_requests_for_flag_response = launchdarkly.approvals.list_requests_for_flag(
    project_key="projectKey_example",
    feature_flag_key="featureFlagKey_example",
    environment_key="environmentKey_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### feature_flag_key: `str`<a id="feature_flag_key-str"></a>

The feature flag key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

#### 🔄 Return<a id="🔄-return"></a>

[`FlagConfigApprovalRequestsResponse`](./launch_darkly_python_sdk/pydantic/flag_config_approval_requests_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/projects/{projectKey}/flags/{featureFlagKey}/environments/{environmentKey}/approval-requests` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.approvals.review_flag_request`<a id="launchdarklyapprovalsreview_flag_request"></a>

Review an approval request by approving or denying changes.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
review_flag_request_response = launchdarkly.approvals.review_flag_request(
    project_key="projectKey_example",
    feature_flag_key="featureFlagKey_example",
    environment_key="environmentKey_example",
    id="id_example",
    kind="approve",
    comment="Looks good, thanks for updating",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### feature_flag_key: `str`<a id="feature_flag_key-str"></a>

The feature flag key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

##### id: `str`<a id="id-str"></a>

The feature flag approval request ID

##### kind: `str`<a id="kind-str"></a>

The type of review for this approval request

##### comment: `str`<a id="comment-str"></a>

Optional comment about the approval request

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`PostApprovalRequestReviewRequest`](./launch_darkly_python_sdk/type/post_approval_request_review_request.py)
#### 🔄 Return<a id="🔄-return"></a>

[`FlagConfigApprovalRequestResponse`](./launch_darkly_python_sdk/pydantic/flag_config_approval_request_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/projects/{projectKey}/flags/{featureFlagKey}/environments/{environmentKey}/approval-requests/{id}/reviews` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.approvals.review_request`<a id="launchdarklyapprovalsreview_request"></a>

Review an approval request by approving or denying changes.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
review_request_response = launchdarkly.approvals.review_request(
    id="id_example",
    kind="approve",
    comment="Looks good, thanks for updating",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

The approval request ID

##### kind: `str`<a id="kind-str"></a>

The type of review for this approval request

##### comment: `str`<a id="comment-str"></a>

Optional comment about the approval request

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`PostApprovalRequestReviewRequest`](./launch_darkly_python_sdk/type/post_approval_request_review_request.py)
#### 🔄 Return<a id="🔄-return"></a>

[`ApprovalRequestResponse`](./launch_darkly_python_sdk/pydantic/approval_request_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/approval-requests/{id}/reviews` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.approvals.single_request`<a id="launchdarklyapprovalssingle_request"></a>

Get a single approval request for a feature flag.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
single_request_response = launchdarkly.approvals.single_request(
    project_key="projectKey_example",
    feature_flag_key="featureFlagKey_example",
    environment_key="environmentKey_example",
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### feature_flag_key: `str`<a id="feature_flag_key-str"></a>

The feature flag key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

##### id: `str`<a id="id-str"></a>

The feature flag approval request ID

#### 🔄 Return<a id="🔄-return"></a>

[`FlagConfigApprovalRequestResponse`](./launch_darkly_python_sdk/pydantic/flag_config_approval_request_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/projects/{projectKey}/flags/{featureFlagKey}/environments/{environmentKey}/approval-requests/{id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.audit_log.detail_entry`<a id="launchdarklyaudit_logdetail_entry"></a>

Fetch a detailed audit log entry representation. The detailed representation includes several fields that are not present in the summary representation, including:

- `delta`: the JSON patch body that was used in the request to update the entity
- `previousVersion`: a JSON representation of the previous version of the entity
- `currentVersion`: a JSON representation of the current version of the entity


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
detail_entry_response = launchdarkly.audit_log.detail_entry(
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

The ID of the audit log entry

#### 🔄 Return<a id="🔄-return"></a>

[`AuditLogEntryRep`](./launch_darkly_python_sdk/pydantic/audit_log_entry_rep.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/auditlog/{id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.audit_log.list_audit_log_entries`<a id="launchdarklyaudit_loglist_audit_log_entries"></a>

Get a list of all audit log entries. The query parameters let you restrict the results that return by date ranges, resource specifiers, or a full-text search query.

LaunchDarkly uses a resource specifier syntax to name resources or collections of resources. To learn more, read [Understanding the resource specifier syntax](https://docs.launchdarkly.com/home/members/role-resources#understanding-the-resource-specifier-syntax).


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_audit_log_entries_response = launchdarkly.audit_log.list_audit_log_entries(
    before=1,
    after=1,
    q="string_example",
    limit=1,
    spec="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### before: `int`<a id="before-int"></a>

A timestamp filter, expressed as a Unix epoch time in milliseconds.  All entries this returns occurred before the timestamp.

##### after: `int`<a id="after-int"></a>

A timestamp filter, expressed as a Unix epoch time in milliseconds. All entries this returns occurred after the timestamp.

##### q: `str`<a id="q-str"></a>

Text to search for. You can search for the full or partial name of the resource.

##### limit: `int`<a id="limit-int"></a>

A limit on the number of audit log entries that return. Set between 1 and 20. The default is 10.

##### spec: `str`<a id="spec-str"></a>

A resource specifier that lets you filter audit log listings by resource

#### 🔄 Return<a id="🔄-return"></a>

[`AuditLogEntryListingRepCollection`](./launch_darkly_python_sdk/pydantic/audit_log_entry_listing_rep_collection.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/auditlog` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.code_references.asynchronously_delete_branches`<a id="launchdarklycode_referencesasynchronously_delete_branches"></a>

Asynchronously delete a number of branches.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
launchdarkly.code_references.asynchronously_delete_branches(
    body=["branch-to-be-deleted", "another-branch-to-be-deleted"],
    repo="repo_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### repo: `str`<a id="repo-str"></a>

The repository name to delete branches for.

##### requestBody: [`CodeReferencesAsynchronouslyDeleteBranchesRequest`](./launch_darkly_python_sdk/type/code_references_asynchronously_delete_branches_request.py)<a id="requestbody-codereferencesasynchronouslydeletebranchesrequestlaunch_darkly_python_sdktypecode_references_asynchronously_delete_branches_requestpy"></a>

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/code-refs/repositories/{repo}/branch-delete-tasks` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.code_references.create_extinction`<a id="launchdarklycode_referencescreate_extinction"></a>

Create a new extinction.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
launchdarkly.code_references.create_extinction(
    body=[
        {
            "revision": "a94a8fe5ccb19ba61c4c0873d391e987982fbbd3",
            "message": "Remove flag for launched feature",
            "time": 1,
            "flag_key": "enable-feature",
            "proj_key": "default",
        }
    ],
    repo="repo_example",
    branch="branch_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### repo: `str`<a id="repo-str"></a>

The repository name

##### branch: `str`<a id="branch-str"></a>

The URL-encoded branch name

##### requestBody: [`ExtinctionListPost`](./launch_darkly_python_sdk/type/extinction_list_post.py)<a id="requestbody-extinctionlistpostlaunch_darkly_python_sdktypeextinction_list_postpy"></a>

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/code-refs/repositories/{repo}/branches/{branch}/extinction-events` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.code_references.create_repository`<a id="launchdarklycode_referencescreate_repository"></a>

Create a repository with the specified name.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
create_repository_response = launchdarkly.code_references.create_repository(
    name="LaunchDarkly-Docs",
    source_link="https://github.com/launchdarkly/LaunchDarkly-Docs",
    commit_url_template="https://github.com/launchdarkly/LaunchDarkly-Docs/commit/${sha}",
    hunk_url_template="https://github.com/launchdarkly/LaunchDarkly-Docs/blob/${sha}/${filePath}#L${lineNumber}",
    type="github",
    default_branch="main",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### name: `str`<a id="name-str"></a>

The repository name

##### source_link: `str`<a id="source_link-str"></a>

A URL to access the repository

##### commit_url_template: `str`<a id="commit_url_template-str"></a>

A template for constructing a valid URL to view the commit

##### hunk_url_template: `str`<a id="hunk_url_template-str"></a>

A template for constructing a valid URL to view the hunk

##### type: `str`<a id="type-str"></a>

The type of repository. If not specified, the default value is <code>custom</code>.

##### default_branch: `str`<a id="default_branch-str"></a>

The repository's default branch. If not specified, the default value is <code>main</code>.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`RepositoryPost`](./launch_darkly_python_sdk/type/repository_post.py)
#### 🔄 Return<a id="🔄-return"></a>

[`RepositoryRep`](./launch_darkly_python_sdk/pydantic/repository_rep.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/code-refs/repositories` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.code_references.delete_repository`<a id="launchdarklycode_referencesdelete_repository"></a>

Delete a repository with the specified name.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
launchdarkly.code_references.delete_repository(
    repo="repo_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### repo: `str`<a id="repo-str"></a>

The repository name

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/code-refs/repositories/{repo}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.code_references.get_branch`<a id="launchdarklycode_referencesget_branch"></a>

Get a specific branch in a repository.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_branch_response = launchdarkly.code_references.get_branch(
    repo="repo_example",
    branch="branch_example",
    proj_key="string_example",
    flag_key="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### repo: `str`<a id="repo-str"></a>

The repository name

##### branch: `str`<a id="branch-str"></a>

The url-encoded branch name

##### proj_key: `str`<a id="proj_key-str"></a>

Filter results to a specific project

##### flag_key: `str`<a id="flag_key-str"></a>

Filter results to a specific flag key

#### 🔄 Return<a id="🔄-return"></a>

[`BranchRep`](./launch_darkly_python_sdk/pydantic/branch_rep.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/code-refs/repositories/{repo}/branches/{branch}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.code_references.get_repository_by_repo`<a id="launchdarklycode_referencesget_repository_by_repo"></a>

Get a single repository by name.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_repository_by_repo_response = launchdarkly.code_references.get_repository_by_repo(
    repo="repo_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### repo: `str`<a id="repo-str"></a>

The repository name

#### 🔄 Return<a id="🔄-return"></a>

[`RepositoryRep`](./launch_darkly_python_sdk/pydantic/repository_rep.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/code-refs/repositories/{repo}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.code_references.get_statistics`<a id="launchdarklycode_referencesget_statistics"></a>

Get links for all projects that have code references.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_statistics_response = launchdarkly.code_references.get_statistics()
```

#### 🔄 Return<a id="🔄-return"></a>

[`StatisticsRoot`](./launch_darkly_python_sdk/pydantic/statistics_root.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/code-refs/statistics` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.code_references.get_statistics_0`<a id="launchdarklycode_referencesget_statistics_0"></a>

Get statistics about all the code references across repositories for all flags in your project that have code references in the default branch, for example, `main`. Optionally, you can include the `flagKey` query parameter to limit your request to statistics about code references for a single flag. This endpoint returns the number of references to your flag keys in your repositories, as well as a link to each repository.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_statistics_0_response = launchdarkly.code_references.get_statistics_0(
    project_key="projectKey_example",
    flag_key="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### flag_key: `str`<a id="flag_key-str"></a>

Filter results to a specific flag key

#### 🔄 Return<a id="🔄-return"></a>

[`StatisticCollectionRep`](./launch_darkly_python_sdk/pydantic/statistic_collection_rep.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/code-refs/statistics/{projectKey}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.code_references.list_branches`<a id="launchdarklycode_referenceslist_branches"></a>

Get a list of branches.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_branches_response = launchdarkly.code_references.list_branches(
    repo="repo_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### repo: `str`<a id="repo-str"></a>

The repository name

#### 🔄 Return<a id="🔄-return"></a>

[`BranchCollectionRep`](./launch_darkly_python_sdk/pydantic/branch_collection_rep.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/code-refs/repositories/{repo}/branches` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.code_references.list_extinctions`<a id="launchdarklycode_referenceslist_extinctions"></a>

Get a list of all extinctions. LaunchDarkly creates an extinction event after you remove all code references to a flag. To learn more, read [Understanding extinction events](https://docs.launchdarkly.com/home/code/code-references#understanding-extinction-events).

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_extinctions_response = launchdarkly.code_references.list_extinctions(
    repo_name="string_example",
    branch_name="string_example",
    proj_key="string_example",
    flag_key="string_example",
    _from=1,
    to=1,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### repo_name: `str`<a id="repo_name-str"></a>

Filter results to a specific repository

##### branch_name: `str`<a id="branch_name-str"></a>

Filter results to a specific branch. By default, only the default branch will be queried for extinctions.

##### proj_key: `str`<a id="proj_key-str"></a>

Filter results to a specific project

##### flag_key: `str`<a id="flag_key-str"></a>

Filter results to a specific flag key

##### _from: `int`<a id="_from-int"></a>

Filter results to a specific timeframe based on commit time, expressed as a Unix epoch time in milliseconds. Must be used with `to`.

##### to: `int`<a id="to-int"></a>

Filter results to a specific timeframe based on commit time, expressed as a Unix epoch time in milliseconds. Must be used with `from`.

#### 🔄 Return<a id="🔄-return"></a>

[`ExtinctionCollectionRep`](./launch_darkly_python_sdk/pydantic/extinction_collection_rep.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/code-refs/extinctions` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.code_references.list_repositories`<a id="launchdarklycode_referenceslist_repositories"></a>

Get a list of connected repositories. Optionally, you can include branch metadata with the `withBranches` query parameter. Embed references for the default branch with `ReferencesForDefaultBranch`. You can also filter the list of code references by project key and flag key.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_repositories_response = launchdarkly.code_references.list_repositories(
    with_branches="string_example",
    with_references_for_default_branch="string_example",
    proj_key="string_example",
    flag_key="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### with_branches: `str`<a id="with_branches-str"></a>

If set to any value, the endpoint returns repositories with associated branch data

##### with_references_for_default_branch: `str`<a id="with_references_for_default_branch-str"></a>

If set to any value, the endpoint returns repositories with associated branch data, as well as code references for the default git branch

##### proj_key: `str`<a id="proj_key-str"></a>

A LaunchDarkly project key. If provided, this filters code reference results to the specified project.

##### flag_key: `str`<a id="flag_key-str"></a>

If set to any value, the endpoint returns repositories with associated branch data, as well as code references for the default git branch

#### 🔄 Return<a id="🔄-return"></a>

[`RepositoryCollectionRep`](./launch_darkly_python_sdk/pydantic/repository_collection_rep.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/code-refs/repositories` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.code_references.update_repository_settings`<a id="launchdarklycode_referencesupdate_repository_settings"></a>

Update a repository's settings. Updating repository settings uses a [JSON patch](https://datatracker.ietf.org/doc/html/rfc6902) or [JSON merge patch](https://datatracker.ietf.org/doc/html/rfc7386) representation of the desired changes. To learn more, read [Updates](https://apidocs.launchdarkly.com).

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
update_repository_settings_response = launchdarkly.code_references.update_repository_settings(
    body=[{"op":"replace","path":"/defaultBranch","value":"main"}],
    repo="repo_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### repo: `str`<a id="repo-str"></a>

The repository name

##### requestBody: [`JSONPatch`](./launch_darkly_python_sdk/type/json_patch.py)<a id="requestbody-jsonpatchlaunch_darkly_python_sdktypejson_patchpy"></a>

#### 🔄 Return<a id="🔄-return"></a>

[`RepositoryRep`](./launch_darkly_python_sdk/pydantic/repository_rep.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/code-refs/repositories/{repo}` `patch`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.code_references.upsert_branch`<a id="launchdarklycode_referencesupsert_branch"></a>

Create a new branch if it doesn't exist, or update the branch if it already exists.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
launchdarkly.code_references.upsert_branch(
    name="main",
    head="a94a8fe5ccb19ba61c4c0873d391e987982fbbd3",
    sync_time=1,
    repo="repo_example",
    branch="branch_example",
    update_sequence_id=25,
    references=[
        {
            "path": "/main/index.js",
            "hint": "javascript",
            "hunks": [
                {
                    "starting_line_number": 45,
                    "lines": "var enableFeature = 'enable-feature';",
                    "proj_key": "default",
                    "flag_key": "enable-feature",
                    "aliases": ["enableFeature", "EnableFeature"],
                }
            ],
        }
    ],
    commit_time=1,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### name: `str`<a id="name-str"></a>

The branch name

##### head: `str`<a id="head-str"></a>

An ID representing the branch HEAD. For example, a commit SHA.

##### sync_time: `int`<a id="sync_time-int"></a>

##### repo: `str`<a id="repo-str"></a>

The repository name

##### branch: `str`<a id="branch-str"></a>

The URL-encoded branch name

##### update_sequence_id: `int`<a id="update_sequence_id-int"></a>

An optional ID used to prevent older data from overwriting newer data. If no sequence ID is included, the newly submitted data will always be saved.

##### references: List[`ReferenceRep`]<a id="references-listreferencerep"></a>

An array of flag references found on the branch

##### commit_time: `int`<a id="commit_time-int"></a>

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`PutBranch`](./launch_darkly_python_sdk/type/put_branch.py)
#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/code-refs/repositories/{repo}/branches/{branch}` `put`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.context_settings.update_settings_for_context`<a id="launchdarklycontext_settingsupdate_settings_for_context"></a>


Enable or disable a feature flag for a context based on its context kind and key.

Omitting the `setting` attribute from the request body, or including a `setting` of `null`, erases the current setting for a context.

If you previously patched the flag, and the patch included the context's data, LaunchDarkly continues to use that data. If LaunchDarkly has never encountered the combination of the context's key and kind before, it calculates the flag values based on the context kind and key.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
launchdarkly.context_settings.update_settings_for_context(
    project_key="projectKey_example",
    environment_key="environmentKey_example",
    context_kind="contextKind_example",
    context_key="contextKey_example",
    feature_flag_key="featureFlagKey_example",
    setting=None,
    comment="make sure this context experiences a specific variation",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

##### context_kind: `str`<a id="context_kind-str"></a>

The context kind

##### context_key: `str`<a id="context_key-str"></a>

The context key

##### feature_flag_key: `str`<a id="feature_flag_key-str"></a>

The feature flag key

##### setting: [`Union[bool, date, datetime, dict, float, int, list, str, None]`](./launch_darkly_python_sdk/type/typing_union_bool_date_datetime_dict_float_int_list_str_none.py)<a id="setting-unionbool-date-datetime-dict-float-int-list-str-nonelaunch_darkly_python_sdktypetyping_union_bool_date_datetime_dict_float_int_list_str_nonepy"></a>

The variation value to set for the context. Must match the flag's variation type.

##### comment: `str`<a id="comment-str"></a>

Optional comment describing the change

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`ValuePut`](./launch_darkly_python_sdk/type/value_put.py)
#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/projects/{projectKey}/environments/{environmentKey}/contexts/{contextKind}/{contextKey}/flags/{featureFlagKey}` `put`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.contexts.create_or_update_kind`<a id="launchdarklycontextscreate_or_update_kind"></a>

Create or update a context kind by key. Only the included fields will be updated.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
create_or_update_kind_response = launchdarkly.contexts.create_or_update_kind(
    name="organization",
    project_key="projectKey_example",
    key="key_example",
    description="An example context kind for organizations",
    version=1,
    hide_in_targeting=False,
    archived=False,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### name: `str`<a id="name-str"></a>

The context kind name

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### key: `str`<a id="key-str"></a>

The context kind key

##### description: `str`<a id="description-str"></a>

The context kind description

##### version: `int`<a id="version-int"></a>

The context kind version. If not specified when the context kind is created, defaults to 1.

##### hide_in_targeting: `bool`<a id="hide_in_targeting-bool"></a>

Alias for archived.

##### archived: `bool`<a id="archived-bool"></a>

Whether the context kind is archived. Archived context kinds are unavailable for targeting.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`UpsertContextKindPayload`](./launch_darkly_python_sdk/type/upsert_context_kind_payload.py)
#### 🔄 Return<a id="🔄-return"></a>

[`UpsertResponseRep`](./launch_darkly_python_sdk/pydantic/upsert_response_rep.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/projects/{projectKey}/context-kinds/{key}` `put`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.contexts.delete_context_instance`<a id="launchdarklycontextsdelete_context_instance"></a>

Delete context instances by ID.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
launchdarkly.contexts.delete_context_instance(
    project_key="projectKey_example",
    environment_key="environmentKey_example",
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

##### id: `str`<a id="id-str"></a>

The context instance ID

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/projects/{projectKey}/environments/{environmentKey}/context-instances/{id}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.contexts.evaluate_flags_for_context_instance`<a id="launchdarklycontextsevaluate_flags_for_context_instance"></a>

Evaluate flags for a context instance, for example, to determine the expected flag variation. **Do not use this API instead of an SDK.** The LaunchDarkly SDKs are specialized for the tasks of evaluating feature flags in your application at scale and generating analytics events based on those evaluations. This API is not designed for that use case. Any evaluations you perform with this API will not be reflected in features such as flag statuses and flag insights. Context instances evaluated by this API will not appear in the Contexts list. To learn more, read [Comparing LaunchDarkly's SDKs and REST API](https://docs.launchdarkly.com/guide/api/comparing-sdk-rest-api).

### Filtering <a id="filtering-"></a>

LaunchDarkly supports the `filter` query param for filtering, with the following fields:

- `query` filters for a string that matches against the flags' keys and names. It is not case sensitive. For example: `filter=query equals dark-mode`.
- `tags` filters the list to flags that have all of the tags in the list. For example: `filter=tags contains ["beta","q1"]`.

You can also apply multiple filters at once. For example, setting `filter=query equals dark-mode, tags contains ["beta","q1"]` matches flags which match the key or name `dark-mode` and are tagged `beta` and `q1`.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
evaluate_flags_for_context_instance_response = launchdarkly.contexts.evaluate_flags_for_context_instance(
    project_key="projectKey_example",
    environment_key="environmentKey_example",
    limit=1,
    offset=1,
    sort="string_example",
    filter="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

##### limit: `int`<a id="limit-int"></a>

The number of feature flags to return. Defaults to -1, which returns all flags

##### offset: `int`<a id="offset-int"></a>

Where to start in the list. Use this with pagination. For example, an offset of 10 skips the first ten items and then returns the next items in the list, up to the query `limit`.

##### sort: `str`<a id="sort-str"></a>

A comma-separated list of fields to sort by. Fields prefixed by a dash ( - ) sort in descending order

##### filter: `str`<a id="filter-str"></a>

A comma-separated list of filters. Each filter is of the form `field operator value`. Supported fields are explained above.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`ContextInstance`](./launch_darkly_python_sdk/type/context_instance.py)
#### 🔄 Return<a id="🔄-return"></a>

[`ContextInstanceEvaluations`](./launch_darkly_python_sdk/pydantic/context_instance_evaluations.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/projects/{projectKey}/environments/{environmentKey}/flags/evaluate` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.contexts.get_attribute_names`<a id="launchdarklycontextsget_attribute_names"></a>

Get context attribute names. Returns only the first 100 attribute names per context.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_attribute_names_response = launchdarkly.contexts.get_attribute_names(
    project_key="projectKey_example",
    environment_key="environmentKey_example",
    filter="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

##### filter: `str`<a id="filter-str"></a>

A comma-separated list of context filters. This endpoint only accepts `kind` filters, with the `equals` operator, and `name` filters, with the `startsWith` operator. To learn more about the filter syntax, read [Filtering contexts and context instances](https://apidocs.launchdarkly.com).

#### 🔄 Return<a id="🔄-return"></a>

[`ContextAttributeNamesCollection`](./launch_darkly_python_sdk/pydantic/context_attribute_names_collection.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/projects/{projectKey}/environments/{environmentKey}/context-attributes` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.contexts.get_by_kind_and_key`<a id="launchdarklycontextsget_by_kind_and_key"></a>

Get contexts based on kind and key.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_by_kind_and_key_response = launchdarkly.contexts.get_by_kind_and_key(
    project_key="projectKey_example",
    environment_key="environmentKey_example",
    kind="kind_example",
    key="key_example",
    limit=1,
    continuation_token="string_example",
    sort="string_example",
    filter="string_example",
    include_total_count=True,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

##### kind: `str`<a id="kind-str"></a>

The context kind

##### key: `str`<a id="key-str"></a>

The context key

##### limit: `int`<a id="limit-int"></a>

Specifies the maximum number of items in the collection to return (max: 50, default: 20)

##### continuation_token: `str`<a id="continuation_token-str"></a>

Limits results to contexts with sort values after the value specified. You can use this for pagination, however, we recommend using the `next` link we provide instead.

##### sort: `str`<a id="sort-str"></a>

Specifies a field by which to sort. LaunchDarkly supports sorting by timestamp in ascending order by specifying `ts` for this value, or descending order by specifying `-ts`.

##### filter: `str`<a id="filter-str"></a>

A comma-separated list of context filters. This endpoint only accepts an `applicationId` filter. To learn more about the filter syntax, read [Filtering contexts and context instances](https://apidocs.launchdarkly.com).

##### include_total_count: `bool`<a id="include_total_count-bool"></a>

Specifies whether to include or omit the total count of matching contexts. Defaults to true.

#### 🔄 Return<a id="🔄-return"></a>

[`Contexts`](./launch_darkly_python_sdk/pydantic/contexts.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/projects/{projectKey}/environments/{environmentKey}/contexts/{kind}/{key}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.contexts.get_context_attribute_values`<a id="launchdarklycontextsget_context_attribute_values"></a>

Get context attribute values.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_context_attribute_values_response = launchdarkly.contexts.get_context_attribute_values(
    project_key="projectKey_example",
    environment_key="environmentKey_example",
    attribute_name="attributeName_example",
    filter="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

##### attribute_name: `str`<a id="attribute_name-str"></a>

The attribute name

##### filter: `str`<a id="filter-str"></a>

A comma-separated list of context filters. This endpoint only accepts `kind` filters, with the `equals` operator, and `value` filters, with the `startsWith` operator. To learn more about the filter syntax, read [Filtering contexts and context instances](https://apidocs.launchdarkly.com).

#### 🔄 Return<a id="🔄-return"></a>

[`ContextAttributeValuesCollection`](./launch_darkly_python_sdk/pydantic/context_attribute_values_collection.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/projects/{projectKey}/environments/{environmentKey}/context-attributes/{attributeName}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.contexts.get_context_instances`<a id="launchdarklycontextsget_context_instances"></a>

Get context instances by ID.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_context_instances_response = launchdarkly.contexts.get_context_instances(
    project_key="projectKey_example",
    environment_key="environmentKey_example",
    id="id_example",
    limit=1,
    continuation_token="string_example",
    sort="string_example",
    filter="string_example",
    include_total_count=True,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

##### id: `str`<a id="id-str"></a>

The context instance ID

##### limit: `int`<a id="limit-int"></a>

Specifies the maximum number of context instances to return (max: 50, default: 20)

##### continuation_token: `str`<a id="continuation_token-str"></a>

Limits results to context instances with sort values after the value specified. You can use this for pagination, however, we recommend using the `next` link we provide instead.

##### sort: `str`<a id="sort-str"></a>

Specifies a field by which to sort. LaunchDarkly supports sorting by timestamp in ascending order by specifying `ts` for this value, or descending order by specifying `-ts`.

##### filter: `str`<a id="filter-str"></a>

A comma-separated list of context filters. This endpoint only accepts an `applicationId` filter. To learn more about the filter syntax, read [Filtering contexts and context instances](https://apidocs.launchdarkly.com).

##### include_total_count: `bool`<a id="include_total_count-bool"></a>

Specifies whether to include or omit the total count of matching context instances. Defaults to true.

#### 🔄 Return<a id="🔄-return"></a>

[`ContextInstances`](./launch_darkly_python_sdk/pydantic/context_instances.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/projects/{projectKey}/environments/{environmentKey}/context-instances/{id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.contexts.list_context_kinds_by_project`<a id="launchdarklycontextslist_context_kinds_by_project"></a>

Get all context kinds for a given project.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_context_kinds_by_project_response = launchdarkly.contexts.list_context_kinds_by_project(
    project_key="projectKey_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

#### 🔄 Return<a id="🔄-return"></a>

[`ContextKindsCollectionRep`](./launch_darkly_python_sdk/pydantic/context_kinds_collection_rep.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/projects/{projectKey}/context-kinds` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.contexts.search_context_instances`<a id="launchdarklycontextssearch_context_instances"></a>


Search for context instances.

You can use either the query parameters or the request body parameters. If both are provided, there is an error.

To learn more about the filter syntax, read [Filtering contexts and context instances](https://apidocs.launchdarkly.com). To learn more about context instances, read [Understanding context instances](https://docs.launchdarkly.com/home/contexts#understanding-context-instances).


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
search_context_instances_response = launchdarkly.contexts.search_context_instances(
    project_key="projectKey_example",
    environment_key="environmentKey_example",
    filter="{\"filter\": \"kindKeys:{\"contains\": [\"user:Henry\"]},\"sort\": \"-ts\",\"limit\": 50}",
    sort="-ts",
    limit=10,
    continuation_token="QAGFKH1313KUGI2351",
    limit=1,
    continuation_token="string_example",
    sort="string_example",
    filter="string_example",
    include_total_count=True,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

##### limit: `int`<a id="limit-int"></a>

Specifies the maximum number of items in the collection to return (max: 50, default: 20)

##### continuation_token: `str`<a id="continuation_token-str"></a>

Limits results to context instances with sort values after the value specified. You can use this for pagination, however, we recommend using the `next` link we provide instead.

##### sort: `str`<a id="sort-str"></a>

Specifies a field by which to sort. LaunchDarkly supports sorting by timestamp in ascending order by specifying `ts` for this value, or descending order by specifying `-ts`.

##### filter: `str`<a id="filter-str"></a>

A comma-separated list of context filters. This endpoint only accepts an `applicationId` filter. To learn more about the filter syntax, read [Filtering contexts and context instances](https://apidocs.launchdarkly.com).

##### include_total_count: `bool`<a id="include_total_count-bool"></a>

Specifies whether to include or omit the total count of matching context instances. Defaults to true.

##### requestBody: [`ContextInstanceSearch`](./launch_darkly_python_sdk/type/context_instance_search.py)<a id="requestbody-contextinstancesearchlaunch_darkly_python_sdktypecontext_instance_searchpy"></a>

#### 🔄 Return<a id="🔄-return"></a>

[`ContextInstances`](./launch_darkly_python_sdk/pydantic/context_instances.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/projects/{projectKey}/environments/{environmentKey}/context-instances/search` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.contexts.search_contexts`<a id="launchdarklycontextssearch_contexts"></a>


Search for contexts.

You can use either the query parameters or the request body parameters. If both are provided, there is an error.

To learn more about the filter syntax, read [Filtering contexts and context instances](https://apidocs.launchdarkly.com). To learn more about contexts, read [Understanding contexts and context kinds](https://docs.launchdarkly.com/home/contexts#understanding-contexts-and-context-kinds).


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
search_contexts_response = launchdarkly.contexts.search_contexts(
    project_key="projectKey_example",
    environment_key="environmentKey_example",
    filter="*.name startsWith Jo,kind anyOf [\"user\",\"organization\"]",
    sort="-ts",
    limit=10,
    continuation_token="QAGFKH1313KUGI2351",
    limit=1,
    continuation_token="string_example",
    sort="string_example",
    filter="string_example",
    include_total_count=True,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

##### limit: `int`<a id="limit-int"></a>

Specifies the maximum number of items in the collection to return (max: 50, default: 20)

##### continuation_token: `str`<a id="continuation_token-str"></a>

Limits results to contexts with sort values after the value specified. You can use this for pagination, however, we recommend using the `next` link we provide instead.

##### sort: `str`<a id="sort-str"></a>

Specifies a field by which to sort. LaunchDarkly supports sorting by timestamp in ascending order by specifying `ts` for this value, or descending order by specifying `-ts`.

##### filter: `str`<a id="filter-str"></a>

A comma-separated list of context filters. To learn more about the filter syntax, read [Filtering contexts and context instances](https://apidocs.launchdarkly.com).

##### include_total_count: `bool`<a id="include_total_count-bool"></a>

Specifies whether to include or omit the total count of matching contexts. Defaults to true.

##### requestBody: [`ContextSearch`](./launch_darkly_python_sdk/type/context_search.py)<a id="requestbody-contextsearchlaunch_darkly_python_sdktypecontext_searchpy"></a>

#### 🔄 Return<a id="🔄-return"></a>

[`Contexts`](./launch_darkly_python_sdk/pydantic/contexts.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/projects/{projectKey}/environments/{environmentKey}/contexts/search` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.custom_roles.create_new_role`<a id="launchdarklycustom_rolescreate_new_role"></a>

Create a new custom role

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
create_new_role_response = launchdarkly.custom_roles.create_new_role(
    name="Ops team",
    key="role-key-123abc",
    policy=[
        {
            "resources": ["proj/*:env/*:flag/*;testing-tag"],
            "actions": ["*"],
            "effect": "allow",
        }
    ],
    description="An example role for members of the ops team",
    base_permissions="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### name: `str`<a id="name-str"></a>

A human-friendly name for the custom role

##### key: `str`<a id="key-str"></a>

The custom role key

##### policy: [`StatementPostList`](./launch_darkly_python_sdk/type/statement_post_list.py)<a id="policy-statementpostlistlaunch_darkly_python_sdktypestatement_post_listpy"></a>

##### description: `str`<a id="description-str"></a>

Description of custom role

##### base_permissions: `str`<a id="base_permissions-str"></a>

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`CustomRolePost`](./launch_darkly_python_sdk/type/custom_role_post.py)
#### 🔄 Return<a id="🔄-return"></a>

[`CustomRole`](./launch_darkly_python_sdk/pydantic/custom_role.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/roles` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.custom_roles.delete_role_by_custom_key`<a id="launchdarklycustom_rolesdelete_role_by_custom_key"></a>

Delete a custom role by key

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
launchdarkly.custom_roles.delete_role_by_custom_key(
    custom_role_key="customRoleKey_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### custom_role_key: `str`<a id="custom_role_key-str"></a>

The custom role key

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/roles/{customRoleKey}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.custom_roles.get_by_custom_key`<a id="launchdarklycustom_rolesget_by_custom_key"></a>

Get a single custom role by key or ID

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_by_custom_key_response = launchdarkly.custom_roles.get_by_custom_key(
    custom_role_key="customRoleKey_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### custom_role_key: `str`<a id="custom_role_key-str"></a>

The custom role key or ID

#### 🔄 Return<a id="🔄-return"></a>

[`CustomRole`](./launch_darkly_python_sdk/pydantic/custom_role.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/roles/{customRoleKey}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.custom_roles.list_custom_roles`<a id="launchdarklycustom_roleslist_custom_roles"></a>

Get a complete list of custom roles. Custom roles let you create flexible policies providing fine-grained access control to everything in LaunchDarkly, from feature flags to goals, environments, and teams. With custom roles, it's possible to enforce access policies that meet your exact workflow needs. Custom roles are available to customers on our enterprise plans. If you're interested in learning more about our enterprise plans, contact sales@launchdarkly.com.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_custom_roles_response = launchdarkly.custom_roles.list_custom_roles()
```

#### 🔄 Return<a id="🔄-return"></a>

[`CustomRoles`](./launch_darkly_python_sdk/pydantic/custom_roles.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/roles` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.custom_roles.update_single_custom_role`<a id="launchdarklycustom_rolesupdate_single_custom_role"></a>

Update a single custom role. Updating a custom role uses a [JSON patch](https://datatracker.ietf.org/doc/html/rfc6902) or [JSON merge patch](https://datatracker.ietf.org/doc/html/rfc7386) representation of the desired changes. To learn more, read [Updates](https://apidocs.launchdarkly.com).<br/><br/>To add an element to the `policy` array, set the `path` to `/policy` and then append `/<array index>`. Use `/0` to add to the beginning of the array. Use `/-` to add to the end of the array.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
update_single_custom_role_response = launchdarkly.custom_roles.update_single_custom_role(
    patch=[
        {
            "op": "replace",
            "path": "/exampleField",
            "value": None,
        }
    ],
    custom_role_key="customRoleKey_example",
    comment="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### patch: [`JSONPatch`](./launch_darkly_python_sdk/type/json_patch.py)<a id="patch-jsonpatchlaunch_darkly_python_sdktypejson_patchpy"></a>

##### custom_role_key: `str`<a id="custom_role_key-str"></a>

The custom role key

##### comment: `str`<a id="comment-str"></a>

Optional comment

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`PatchWithComment`](./launch_darkly_python_sdk/type/patch_with_comment.py)
#### 🔄 Return<a id="🔄-return"></a>

[`CustomRole`](./launch_darkly_python_sdk/pydantic/custom_role.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/roles/{customRoleKey}` `patch`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.data_export_destinations.create_destination`<a id="launchdarklydata_export_destinationscreate_destination"></a>


Create a new Data Export destination.

In the `config` request body parameter, the fields required depend on the type of Data Export destination.

<details>
<summary>Click to expand <code>config</code> parameter details</summary>

#### Azure Event Hubs<a id="azure-event-hubs"></a>

To create a Data Export destination with a `kind` of `azure-event-hubs`, the `config` object requires the following fields:

* `namespace`: The Event Hub Namespace name
* `name`: The Event Hub name
* `policyName`: The shared access signature policy name. You can find your policy name in the settings of your Azure Event Hubs Namespace.
* `policyKey`: The shared access signature key. You can find your policy key in the settings of your Azure Event Hubs Namespace.

#### Google Cloud Pub/Sub<a id="google-cloud-pubsub"></a>

To create a Data Export destination with a `kind` of `google-pubsub`, the `config` object requires the following fields:

* `project`: The Google PubSub project ID for the project to publish to
* `topic`: The Google PubSub topic ID for the topic to publish to

#### Amazon Kinesis<a id="amazon-kinesis"></a>

To create a Data Export destination with a `kind` of `kinesis`, the `config` object requires the following fields:

* `region`: The Kinesis stream's AWS region key
* `roleArn`: The Amazon Resource Name (ARN) of the AWS role that will be writing to Kinesis
* `streamName`: The name of the Kinesis stream that LaunchDarkly is sending events to. This is not the ARN of the stream.

#### mParticle<a id="mparticle"></a>

To create a Data Export destination with a `kind` of `mparticle`, the `config` object requires the following fields:

* `apiKey`: The mParticle API key
* `secret`: The mParticle API secret
* `userIdentity`: The type of identifier you use to identify your end users in mParticle
* `anonymousUserIdentity`: The type of identifier you use to identify your anonymous end users in mParticle

#### Segment<a id="segment"></a>

To create a Data Export destination with a `kind` of `segment`, the `config` object requires the following fields:

* `writeKey`: The Segment write key. This is used to authenticate LaunchDarkly's calls to Segment.

</details>


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
create_destination_response = launchdarkly.data_export_destinations.create_destination(
    project_key="projectKey_example",
    environment_key="environmentKey_example",
    name="example-destination",
    kind="google-pubsub",
    config=None,
    _true=True,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

##### name: `str`<a id="name-str"></a>

A human-readable name for your Data Export destination

##### kind: `str`<a id="kind-str"></a>

The type of Data Export destination

##### config: [`Union[bool, date, datetime, dict, float, int, list, str, None]`](./launch_darkly_python_sdk/type/typing_union_bool_date_datetime_dict_float_int_list_str_none.py)<a id="config-unionbool-date-datetime-dict-float-int-list-str-nonelaunch_darkly_python_sdktypetyping_union_bool_date_datetime_dict_float_int_list_str_nonepy"></a>

An object with the configuration parameters required for the destination type

##### _true: `bool`<a id="_true-bool"></a>

Whether the export is on. Displayed as the integration status in the LaunchDarkly UI.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`DestinationPost`](./launch_darkly_python_sdk/type/destination_post.py)
#### 🔄 Return<a id="🔄-return"></a>

[`Destination`](./launch_darkly_python_sdk/pydantic/destination.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/destinations/{projectKey}/{environmentKey}` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.data_export_destinations.delete_by_id`<a id="launchdarklydata_export_destinationsdelete_by_id"></a>

Delete a Data Export destination by ID.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
launchdarkly.data_export_destinations.delete_by_id(
    project_key="projectKey_example",
    environment_key="environmentKey_example",
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

##### id: `str`<a id="id-str"></a>

The Data Export destination ID

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/destinations/{projectKey}/{environmentKey}/{id}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.data_export_destinations.get_all`<a id="launchdarklydata_export_destinationsget_all"></a>

Get a list of Data Export destinations configured across all projects and environments.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_all_response = launchdarkly.data_export_destinations.get_all()
```

#### 🔄 Return<a id="🔄-return"></a>

[`Destinations`](./launch_darkly_python_sdk/pydantic/destinations.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/destinations` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.data_export_destinations.get_single_by_id`<a id="launchdarklydata_export_destinationsget_single_by_id"></a>

Get a single Data Export destination by ID.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_single_by_id_response = launchdarkly.data_export_destinations.get_single_by_id(
    project_key="projectKey_example",
    environment_key="environmentKey_example",
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

##### id: `str`<a id="id-str"></a>

The Data Export destination ID

#### 🔄 Return<a id="🔄-return"></a>

[`Destination`](./launch_darkly_python_sdk/pydantic/destination.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/destinations/{projectKey}/{environmentKey}/{id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.data_export_destinations.update_destination_patch`<a id="launchdarklydata_export_destinationsupdate_destination_patch"></a>

Update a Data Export destination. Updating a destination uses a [JSON patch](https://datatracker.ietf.org/doc/html/rfc6902) or [JSON merge patch](https://datatracker.ietf.org/doc/html/rfc7386) representation of the desired changes. To learn more, read [Updates](https://apidocs.launchdarkly.com).

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
update_destination_patch_response = launchdarkly.data_export_destinations.update_destination_patch(
    body=[{"op":"replace","path":"/config/topic","value":"ld-pubsub-test-192302"}],
    project_key="projectKey_example",
    environment_key="environmentKey_example",
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

##### id: `str`<a id="id-str"></a>

The Data Export destination ID

##### requestBody: [`JSONPatch`](./launch_darkly_python_sdk/type/json_patch.py)<a id="requestbody-jsonpatchlaunch_darkly_python_sdktypejson_patchpy"></a>

#### 🔄 Return<a id="🔄-return"></a>

[`Destination`](./launch_darkly_python_sdk/pydantic/destination.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/destinations/{projectKey}/{environmentKey}/{id}` `patch`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.environments.create_new_environment`<a id="launchdarklyenvironmentscreate_new_environment"></a>

> ### Approval settings
>
> The `approvalSettings` key is only returned when the Flag Approvals feature is enabled.
>
> You cannot update approval settings when creating new environments. Update approval settings with the PATCH Environment API.

Create a new environment in a specified project with a given name, key, swatch color, and default TTL.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
create_new_environment_response = launchdarkly.environments.create_new_environment(
    name="My Environment",
    key="environment-key-123abc",
    color="F5A623",
    project_key="projectKey_example",
    tags=["ops"],
    default_ttl=5,
    secure_mode=True,
    default_track_events=False,
    confirm_changes=False,
    require_comments=False,
    source={
    },
    critical=True,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### name: `str`<a id="name-str"></a>

A human-friendly name for the new environment

##### key: `str`<a id="key-str"></a>

A project-unique key for the new environment

##### color: `str`<a id="color-str"></a>

A color to indicate this environment in the UI

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### tags: [`EnvironmentPostTags`](./launch_darkly_python_sdk/type/environment_post_tags.py)<a id="tags-environmentposttagslaunch_darkly_python_sdktypeenvironment_post_tagspy"></a>

##### default_ttl: `int`<a id="default_ttl-int"></a>

The default time (in minutes) that the PHP SDK can cache feature flag rules locally

##### secure_mode: `bool`<a id="secure_mode-bool"></a>

Ensures that one end user of the client-side SDK cannot inspect the variations for another end user

##### default_track_events: `bool`<a id="default_track_events-bool"></a>

Enables tracking detailed information for new flags by default

##### confirm_changes: `bool`<a id="confirm_changes-bool"></a>

Requires confirmation for all flag and segment changes via the UI in this environment

##### require_comments: `bool`<a id="require_comments-bool"></a>

Requires comments for all flag and segment changes via the UI in this environment

##### source: [`SourceEnv`](./launch_darkly_python_sdk/type/source_env.py)<a id="source-sourceenvlaunch_darkly_python_sdktypesource_envpy"></a>


##### critical: `bool`<a id="critical-bool"></a>

Whether the environment is critical

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`EnvironmentPost`](./launch_darkly_python_sdk/type/environment_post.py)
#### 🔄 Return<a id="🔄-return"></a>

[`Environment`](./launch_darkly_python_sdk/pydantic/environment.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/projects/{projectKey}/environments` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.environments.get_by_project_and_key`<a id="launchdarklyenvironmentsget_by_project_and_key"></a>

> ### Approval settings
>
> The `approvalSettings` key is only returned when the Flag Approvals feature is enabled.

Get an environment given a project and key.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_by_project_and_key_response = launchdarkly.environments.get_by_project_and_key(
    project_key="projectKey_example",
    environment_key="environmentKey_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

#### 🔄 Return<a id="🔄-return"></a>

[`Environment`](./launch_darkly_python_sdk/pydantic/environment.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/projects/{projectKey}/environments/{environmentKey}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.environments.list_environments`<a id="launchdarklyenvironmentslist_environments"></a>

Return a list of environments for the specified project.

By default, this returns the first 20 environments. Page through this list with the `limit` parameter and by following the `first`, `prev`, `next`, and `last` links in the `_links` field that returns. If those links do not appear, the pages they refer to don't exist. For example, the `first` and `prev` links will be missing from the response on the first page, because there is no previous page and you cannot return to the first page when you are already on the first page.

### Filtering environments<a id="filtering-environments"></a>

LaunchDarkly supports two fields for filters:
- `query` is a string that matches against the environments' names and keys. It is not case sensitive.
- `tags` is a `+`-separated list of environment tags. It filters the list of environments that have all of the tags in the list.

For example, the filter `filter=query:abc,tags:tag-1+tag-2` matches environments with the string `abc` in their name or key and also are tagged with `tag-1` and `tag-2`. The filter is not case-sensitive.

The documented values for `filter` query parameters are prior to URL encoding. For example, the `+` in `filter=tags:tag-1+tag-2` must be encoded to `%2B`.

### Sorting environments<a id="sorting-environments"></a>

LaunchDarkly supports the following fields for sorting:

- `createdOn` sorts by the creation date of the environment.
- `critical` sorts by whether the environments are marked as critical.
- `name` sorts by environment name.

For example, `sort=name` sorts the response by environment name in ascending order.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_environments_response = launchdarkly.environments.list_environments(
    project_key="projectKey_example",
    limit=1,
    offset=1,
    filter="string_example",
    sort="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### limit: `int`<a id="limit-int"></a>

The number of environments to return in the response. Defaults to 20.

##### offset: `int`<a id="offset-int"></a>

Where to start in the list. This is for use with pagination. For example, an offset of 10 skips the first ten items and then returns the next items in the list, up to the query `limit`.

##### filter: `str`<a id="filter-str"></a>

A comma-separated list of filters. Each filter is of the form `field:value`.

##### sort: `str`<a id="sort-str"></a>

A comma-separated list of fields to sort by. Fields prefixed by a dash ( - ) sort in descending order.

#### 🔄 Return<a id="🔄-return"></a>

[`Environments`](./launch_darkly_python_sdk/pydantic/environments.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/projects/{projectKey}/environments` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.environments.remove_by_environment_key`<a id="launchdarklyenvironmentsremove_by_environment_key"></a>

Delete a environment by key.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
launchdarkly.environments.remove_by_environment_key(
    project_key="projectKey_example",
    environment_key="environmentKey_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/projects/{projectKey}/environments/{environmentKey}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.environments.reset_mobile_sdk_key`<a id="launchdarklyenvironmentsreset_mobile_sdk_key"></a>

Reset an environment's mobile key. The optional expiry for the old key is deprecated for this endpoint, so the old key will always expire immediately.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
reset_mobile_sdk_key_response = launchdarkly.environments.reset_mobile_sdk_key(
    project_key="projectKey_example",
    environment_key="environmentKey_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

#### 🔄 Return<a id="🔄-return"></a>

[`Environment`](./launch_darkly_python_sdk/pydantic/environment.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/projects/{projectKey}/environments/{environmentKey}/mobileKey` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.environments.reset_sdk_key`<a id="launchdarklyenvironmentsreset_sdk_key"></a>

Reset an environment's SDK key with an optional expiry time for the old key.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
reset_sdk_key_response = launchdarkly.environments.reset_sdk_key(
    project_key="projectKey_example",
    environment_key="environmentKey_example",
    expiry=1,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

##### expiry: `int`<a id="expiry-int"></a>

The time at which you want the old SDK key to expire, in UNIX milliseconds. By default, the key expires immediately. During the period between this call and the time when the old SDK key expires, both the old SDK key and the new SDK key will work.

#### 🔄 Return<a id="🔄-return"></a>

[`Environment`](./launch_darkly_python_sdk/pydantic/environment.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/projects/{projectKey}/environments/{environmentKey}/apiKey` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.environments.update_environment_patch`<a id="launchdarklyenvironmentsupdate_environment_patch"></a>


Update an environment. Updating an environment uses a [JSON patch](https://datatracker.ietf.org/doc/html/rfc6902) representation of the desired changes. To learn more, read [Updates](https://apidocs.launchdarkly.com).

To update fields in the environment object that are arrays, set the `path` to the name of the field and then append `/<array index>`. Using `/0` appends to the beginning of the array.

### Approval settings<a id="approval-settings"></a>

This request only returns the `approvalSettings` key if the [Flag Approvals](https://docs.launchdarkly.com/home/feature-workflows/approvals) feature is enabled.

Only the `canReviewOwnRequest`, `canApplyDeclinedChanges`, `minNumApprovals`, `required` and `requiredApprovalTagsfields` are editable.

If you try to patch the environment by setting both `required` and `requiredApprovalTags`, the request fails and an error appears. You can specify either required approvals for all flags in an environment or those with specific tags, but not both.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
update_environment_patch_response = launchdarkly.environments.update_environment_patch(
    body=[{"op":"replace","path":"/requireComments","value":true}],
    project_key="projectKey_example",
    environment_key="environmentKey_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

##### requestBody: [`JSONPatch`](./launch_darkly_python_sdk/type/json_patch.py)<a id="requestbody-jsonpatchlaunch_darkly_python_sdktypejson_patchpy"></a>

#### 🔄 Return<a id="🔄-return"></a>

[`Environment`](./launch_darkly_python_sdk/pydantic/environment.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/projects/{projectKey}/environments/{environmentKey}` `patch`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.experiments_(beta).create_iteration`<a id="launchdarklyexperiments_betacreate_iteration"></a>

Create an experiment iteration.

Experiment iterations let you record experiments in individual blocks of time. Initially, iterations are created with a status of `not_started` and appear in the `draftIteration` field of an experiment. To start or stop an iteration, [update the experiment](https://apidocs.launchdarkly.com)#operation/patchExperiment) with the `startIteration` or `stopIteration` instruction. 

To learn more, read [Starting experiment iterations](https://docs.launchdarkly.com/home/creating-experiments#starting-experiment-iterations).


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
create_iteration_response = launchdarkly.experiments_(beta).create_iteration(
    hypothesis="Example hypothesis, the new button placement will increase conversion",
    metrics=[
        {
            "key": "metric-key-123abc",
            "is_group": True,
            "primary": True,
        }
    ],
    treatments=[
        {
            "parameters": [
                {
                    "flag_key": "example-flag-for-experiment",
                    "variation_id": "e432f62b-55f6-49dd-a02f-eb24acf39d05",
                }
            ],
            "name": "Treatment 1",
            "baseline": True,
            "allocation_percent": "10",
        }
    ],
    flags={
        "key": {
            "rule_id": "e432f62b-55f6-49dd-a02f-eb24acf39d05",
            "flag_config_version": 12,
        },
    },
    project_key="projectKey_example",
    environment_key="environmentKey_example",
    experiment_key="experimentKey_example",
    can_reshuffle_traffic=True,
    primary_single_metric_key="metric-key-123abc",
    primary_funnel_key="metric-group-key-123abc",
    randomization_unit="user",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### hypothesis: `str`<a id="hypothesis-str"></a>

The expected outcome of this experiment

##### metrics: [`MetricsInput`](./launch_darkly_python_sdk/type/metrics_input.py)<a id="metrics-metricsinputlaunch_darkly_python_sdktypemetrics_inputpy"></a>

##### treatments: [`TreatmentsInput`](./launch_darkly_python_sdk/type/treatments_input.py)<a id="treatments-treatmentsinputlaunch_darkly_python_sdktypetreatments_inputpy"></a>

##### flags: [`FlagsInput`](./launch_darkly_python_sdk/type/flags_input.py)<a id="flags-flagsinputlaunch_darkly_python_sdktypeflags_inputpy"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

##### experiment_key: `str`<a id="experiment_key-str"></a>

The experiment key

##### can_reshuffle_traffic: `bool`<a id="can_reshuffle_traffic-bool"></a>

Whether to allow the experiment to reassign traffic to different variations when you increase or decrease the traffic in your experiment audience (true) or keep all traffic assigned to its initial variation (false). Defaults to true.

##### primary_single_metric_key: `str`<a id="primary_single_metric_key-str"></a>

The key of the primary metric for this experiment. Either <code>primarySingleMetricKey</code> or <code>primaryFunnelKey</code> must be present.

##### primary_funnel_key: `str`<a id="primary_funnel_key-str"></a>

The key of the primary funnel group for this experiment. Either <code>primarySingleMetricKey</code> or <code>primaryFunnelKey</code> must be present.

##### randomization_unit: `str`<a id="randomization_unit-str"></a>

The unit of randomization for this iteration. Defaults to user.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`IterationInput`](./launch_darkly_python_sdk/type/iteration_input.py)
#### 🔄 Return<a id="🔄-return"></a>

[`IterationRep`](./launch_darkly_python_sdk/pydantic/iteration_rep.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/projects/{projectKey}/environments/{environmentKey}/experiments/{experimentKey}/iterations` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.experiments_(beta).create_new`<a id="launchdarklyexperiments_betacreate_new"></a>

Create an experiment.

To run this experiment, you'll need to [create an iteration](https://apidocs.launchdarkly.com)#operation/createIteration) and then [update the experiment](https://apidocs.launchdarkly.com)#operation/patchExperiment) with the `startIteration` instruction.

To learn more, read [Creating experiments](https://docs.launchdarkly.com/home/creating-experiments).


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
create_new_response = launchdarkly.experiments_(beta).create_new(
    name="Example experiment",
    key="experiment-key-123abc",
    iteration={
        "hypothesis": "Example hypothesis, the new button placement will increase conversion",
        "can_reshuffle_traffic": True,
        "metrics": [
            {
                "key": "metric-key-123abc",
                "is_group": True,
                "primary": True,
            }
        ],
        "primary_single_metric_key": "metric-key-123abc",
        "primary_funnel_key": "metric-group-key-123abc",
        "treatments": [
            {
                "parameters": [
                    {
                        "flag_key": "example-flag-for-experiment",
                        "variation_id": "e432f62b-55f6-49dd-a02f-eb24acf39d05",
                    }
                ],
                "name": "Treatment 1",
                "baseline": True,
                "allocation_percent": "10",
            }
        ],
        "flags": {
            "key": {
                "rule_id": "e432f62b-55f6-49dd-a02f-eb24acf39d05",
                "flag_config_version": 12,
            },
        },
        "randomization_unit": "user",
    },
    project_key="projectKey_example",
    environment_key="environmentKey_example",
    description="An example experiment, used in testing",
    maintainer_id="12ab3c45de678910fgh12345",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### name: `str`<a id="name-str"></a>

The experiment name

##### key: `str`<a id="key-str"></a>

The experiment key

##### iteration: [`IterationInput`](./launch_darkly_python_sdk/type/iteration_input.py)<a id="iteration-iterationinputlaunch_darkly_python_sdktypeiteration_inputpy"></a>


##### project_key: `str`<a id="project_key-str"></a>

The project key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

##### description: `str`<a id="description-str"></a>

The experiment description

##### maintainer_id: `str`<a id="maintainer_id-str"></a>

The ID of the member who maintains this experiment

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`ExperimentPost`](./launch_darkly_python_sdk/type/experiment_post.py)
#### 🔄 Return<a id="🔄-return"></a>

[`Experiment`](./launch_darkly_python_sdk/pydantic/experiment.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/projects/{projectKey}/environments/{environmentKey}/experiments` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.experiments_(beta).get_details`<a id="launchdarklyexperiments_betaget_details"></a>

Get details about an experiment.

### Expanding the experiment response<a id="expanding-the-experiment-response"></a>

LaunchDarkly supports four fields for expanding the "Get experiment" response. By default, these fields are **not** included in the response.

To expand the response, append the `expand` query parameter and add a comma-separated list with any of the following fields:

- `previousIterations` includes all iterations prior to the current iteration. By default only the current iteration is included in the response.
- `draftIteration` includes the iteration which has not been started yet, if any.
- `secondaryMetrics` includes secondary metrics. By default only the primary metric is included in the response.
- `treatments` includes all treatment and parameter details. By default treatment data is not included in the response.

For example, `expand=draftIteration,treatments` includes the `draftIteration` and `treatments` fields in the response. If fields that you request with the `expand` query parameter are empty, they are not included in the response.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_details_response = launchdarkly.experiments_(beta).get_details(
    project_key="projectKey_example",
    environment_key="environmentKey_example",
    experiment_key="experimentKey_example",
    expand="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

##### experiment_key: `str`<a id="experiment_key-str"></a>

The experiment key

##### expand: `str`<a id="expand-str"></a>

A comma-separated list of properties that can reveal additional information in the response. Supported fields are explained above.

#### 🔄 Return<a id="🔄-return"></a>

[`Experiment`](./launch_darkly_python_sdk/pydantic/experiment.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/projects/{projectKey}/environments/{environmentKey}/experiments/{experimentKey}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.experiments_(beta).get_experiment_metric_results`<a id="launchdarklyexperiments_betaget_experiment_metric_results"></a>

Get results from an experiment for a particular metric.

LaunchDarkly supports one field for expanding the "Get experiment results" response. By default, this field is **not** included in the response.

To expand the response, append the `expand` query parameter with the following field:
* `traffic` includes the total count of units for each treatment.

For example, `expand=traffic` includes the `traffic` field for the project in the response.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_experiment_metric_results_response = launchdarkly.experiments_(beta).get_experiment_metric_results(
    project_key="projectKey_example",
    environment_key="environmentKey_example",
    experiment_key="experimentKey_example",
    metric_key="metricKey_example",
    iteration_id="string_example",
    expand="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

##### experiment_key: `str`<a id="experiment_key-str"></a>

The experiment key

##### metric_key: `str`<a id="metric_key-str"></a>

The metric key

##### iteration_id: `str`<a id="iteration_id-str"></a>

The iteration ID

##### expand: `str`<a id="expand-str"></a>

A comma-separated list of fields to expand in the response. Supported fields are explained above.

#### 🔄 Return<a id="🔄-return"></a>

[`ExperimentBayesianResultsRep`](./launch_darkly_python_sdk/pydantic/experiment_bayesian_results_rep.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/projects/{projectKey}/environments/{environmentKey}/experiments/{experimentKey}/metrics/{metricKey}/results` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.experiments_(beta).get_experimentation_settings`<a id="launchdarklyexperiments_betaget_experimentation_settings"></a>

Get current experimentation settings for the given project

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_experimentation_settings_response = launchdarkly.experiments_(beta).get_experimentation_settings(
    project_key="projectKey_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

#### 🔄 Return<a id="🔄-return"></a>

[`RandomizationSettingsRep`](./launch_darkly_python_sdk/pydantic/randomization_settings_rep.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/projects/{projectKey}/experimentation-settings` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.experiments_(beta).get_legacy_experiment_results`<a id="launchdarklyexperiments_betaget_legacy_experiment_results"></a>

Get detailed experiment result data for legacy experiments.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_legacy_experiment_results_response = launchdarkly.experiments_(beta).get_legacy_experiment_results(
    project_key="projectKey_example",
    feature_flag_key="featureFlagKey_example",
    environment_key="environmentKey_example",
    metric_key="metricKey_example",
    _from=1,
    to=1,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### feature_flag_key: `str`<a id="feature_flag_key-str"></a>

The feature flag key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

##### metric_key: `str`<a id="metric_key-str"></a>

The metric key

##### _from: `int`<a id="_from-int"></a>

A timestamp denoting the start of the data collection period, expressed as a Unix epoch time in milliseconds.

##### to: `int`<a id="to-int"></a>

A timestamp denoting the end of the data collection period, expressed as a Unix epoch time in milliseconds.

#### 🔄 Return<a id="🔄-return"></a>

[`ExperimentResults`](./launch_darkly_python_sdk/pydantic/experiment_results.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/flags/{projectKey}/{featureFlagKey}/experiments/{environmentKey}/{metricKey}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.experiments_(beta).get_results_for_metric_group`<a id="launchdarklyexperiments_betaget_results_for_metric_group"></a>

Get results from an experiment for a particular metric group.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_results_for_metric_group_response = launchdarkly.experiments_(beta).get_results_for_metric_group(
    project_key="projectKey_example",
    environment_key="environmentKey_example",
    experiment_key="experimentKey_example",
    metric_group_key="metricGroupKey_example",
    iteration_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

##### experiment_key: `str`<a id="experiment_key-str"></a>

The experiment key

##### metric_group_key: `str`<a id="metric_group_key-str"></a>

The metric group key

##### iteration_id: `str`<a id="iteration_id-str"></a>

The iteration ID

#### 🔄 Return<a id="🔄-return"></a>

[`MetricGroupResultsRep`](./launch_darkly_python_sdk/pydantic/metric_group_results_rep.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/projects/{projectKey}/environments/{environmentKey}/experiments/{experimentKey}/metric-groups/{metricGroupKey}/results` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.experiments_(beta).list_experiments_in_environment`<a id="launchdarklyexperiments_betalist_experiments_in_environment"></a>

Get details about all experiments in an environment.

### Filtering experiments<a id="filtering-experiments"></a>

LaunchDarkly supports the `filter` query param for filtering, with the following fields:

- `flagKey` filters for only experiments that use the flag with the given key.
- `metricKey` filters for only experiments that use the metric with the given key.
- `status` filters for only experiments with an iteration with the given status. An iteration can have the status `not_started`, `running` or `stopped`.

For example, `filter=flagKey:my-flag,status:running,metricKey:page-load-ms` filters for experiments for the given flag key and the given metric key which have a currently running iteration.

### Expanding the experiments response<a id="expanding-the-experiments-response"></a>

LaunchDarkly supports four fields for expanding the "Get experiments" response. By default, these fields are **not** included in the response.

To expand the response, append the `expand` query parameter and add a comma-separated list with any of the following fields:

- `previousIterations` includes all iterations prior to the current iteration. By default only the current iteration is included in the response.
- `draftIteration` includes the iteration which has not been started yet, if any.
- `secondaryMetrics` includes secondary metrics. By default only the primary metric is included in the response.
- `treatments` includes all treatment and parameter details. By default treatment data is not included in the response.

For example, `expand=draftIteration,treatments` includes the `draftIteration` and `treatments` fields in the response. If fields that you request with the `expand` query parameter are empty, they are not included in the response.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_experiments_in_environment_response = launchdarkly.experiments_(beta).list_experiments_in_environment(
    project_key="projectKey_example",
    environment_key="environmentKey_example",
    limit=1,
    offset=1,
    filter="string_example",
    expand="string_example",
    lifecycle_state="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

##### limit: `int`<a id="limit-int"></a>

The maximum number of experiments to return. Defaults to 20.

##### offset: `int`<a id="offset-int"></a>

Where to start in the list. Use this with pagination. For example, an offset of 10 skips the first ten items and then returns the next items in the list, up to the query `limit`.

##### filter: `str`<a id="filter-str"></a>

A comma-separated list of filters. Each filter is of the form `field:value`. Supported fields are explained above.

##### expand: `str`<a id="expand-str"></a>

A comma-separated list of properties that can reveal additional information in the response. Supported fields are explained above.

##### lifecycle_state: `str`<a id="lifecycle_state-str"></a>

A comma-separated list of experiment archived states. Supports `archived`, `active`, or both. Defaults to `active` experiments.

#### 🔄 Return<a id="🔄-return"></a>

[`ExperimentCollectionRep`](./launch_darkly_python_sdk/pydantic/experiment_collection_rep.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/projects/{projectKey}/environments/{environmentKey}/experiments` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.experiments_(beta).update_experimentation_settings`<a id="launchdarklyexperiments_betaupdate_experimentation_settings"></a>

Update experimentation settings for the given project

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
update_experimentation_settings_response = launchdarkly.experiments_(beta).update_experimentation_settings(
    randomization_units=[
        {
            "randomization_unit": "user",
            "default": True,
            "standard_randomization_unit": "guest",
        }
    ],
    project_key="projectKey_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### randomization_units: List[`RandomizationUnitInput`]<a id="randomization_units-listrandomizationunitinput"></a>

An array of randomization units allowed for this project.

##### project_key: `str`<a id="project_key-str"></a>

The project key

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`RandomizationSettingsPut`](./launch_darkly_python_sdk/type/randomization_settings_put.py)
#### 🔄 Return<a id="🔄-return"></a>

[`RandomizationSettingsRep`](./launch_darkly_python_sdk/pydantic/randomization_settings_rep.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/projects/{projectKey}/experimentation-settings` `put`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.experiments_(beta).update_semantic_patch`<a id="launchdarklyexperiments_betaupdate_semantic_patch"></a>

Update an experiment. Updating an experiment uses the semantic patch format.

To make a semantic patch request, you must append `domain-model=launchdarkly.semanticpatch` to your `Content-Type` header. To learn more, read [Updates using semantic patch](https://apidocs.launchdarkly.com).

### Instructions<a id="instructions"></a>

Semantic patch requests support the following `kind` instructions for updating experiments.

#### updateName<a id="updatename"></a>

Updates the experiment name.

##### Parameters<a id="parameters"></a>

- `value`: The new name.

Here's an example:

```json
{
  "instructions": [{
    "kind": "updateName",
    "value": "Example updated experiment name"
  }]
}
```

#### updateDescription<a id="updatedescription"></a>

Updates the experiment description.

##### Parameters<a id="parameters"></a>

- `value`: The new description.

Here's an example:

```json
{
  "instructions": [{
    "kind": "updateDescription",
    "value": "Example updated description"
  }]
}
```

#### startIteration<a id="startiteration"></a>

Starts a new iteration for this experiment. You must [create a new iteration](https://apidocs.launchdarkly.com)#operation/createIteration) before calling this instruction.

An iteration may not be started until it meets the following criteria:

* Its associated flag is toggled on and is not archived
* Its `randomizationUnit` is set
* At least one of its `treatments` has a non-zero `allocationPercent`

##### Parameters<a id="parameters"></a>

- `changeJustification`: The reason for starting a new iteration. Required when you call `startIteration` on an already running experiment, otherwise optional.

Here's an example:

```json
{
  "instructions": [{
    "kind": "startIteration",
    "changeJustification": "It's time to start a new iteration"
  }]
}
```

#### stopIteration<a id="stopiteration"></a>

Stops the current iteration for this experiment.

##### Parameters<a id="parameters"></a>

- `winningTreatmentId`: The ID of the winning treatment. Treatment IDs are returned as part of the [Get experiment](https://apidocs.launchdarkly.com)#operation/getExperiment) response. They are the `_id` of each element in the `treatments` array.
- `winningReason`: The reason for the winner

Here's an example:

```json
{
  "instructions": [{
    "kind": "stopIteration",
    "winningTreatmentId": "3a548ec2-72ac-4e59-8518-5c24f5609ccf",
    "winningReason": "Example reason to stop the iteration"
  }]
}
```

#### archiveExperiment<a id="archiveexperiment"></a>

Archives this experiment. Archived experiments are hidden by default in the LaunchDarkly user interface. You cannot start new iterations for archived experiments.

Here's an example:

```json
{
  "instructions": [{ "kind": "archiveExperiment" }]
}
```

#### restoreExperiment<a id="restoreexperiment"></a>

Restores an archived experiment. After restoring an experiment, you can start new iterations for it again.

Here's an example:

```json
{
  "instructions": [{ "kind": "restoreExperiment" }]
}
```


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
update_semantic_patch_response = launchdarkly.experiments_(beta).update_semantic_patch(
    instructions=[
        {
            "key": None,
        }
    ],
    project_key="projectKey_example",
    environment_key="environmentKey_example",
    experiment_key="experimentKey_example",
    comment="Optional comment",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### instructions: [`Instructions`](./launch_darkly_python_sdk/type/instructions.py)<a id="instructions-instructionslaunch_darkly_python_sdktypeinstructionspy"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

##### experiment_key: `str`<a id="experiment_key-str"></a>

The experiment key

##### comment: `str`<a id="comment-str"></a>

Optional comment describing the update

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`ExperimentPatchInput`](./launch_darkly_python_sdk/type/experiment_patch_input.py)
#### 🔄 Return<a id="🔄-return"></a>

[`Experiment`](./launch_darkly_python_sdk/pydantic/experiment.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/projects/{projectKey}/environments/{environmentKey}/experiments/{experimentKey}` `patch`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.feature_flags.across_environments`<a id="launchdarklyfeature_flagsacross_environments"></a>

Get the status for a particular feature flag across environments.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
across_environments_response = launchdarkly.feature_flags.across_environments(
    project_key="projectKey_example",
    feature_flag_key="featureFlagKey_example",
    env="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### feature_flag_key: `str`<a id="feature_flag_key-str"></a>

The feature flag key

##### env: `str`<a id="env-str"></a>

Optional environment filter

#### 🔄 Return<a id="🔄-return"></a>

[`FeatureFlagStatusAcrossEnvironments`](./launch_darkly_python_sdk/pydantic/feature_flag_status_across_environments.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/flag-status/{projectKey}/{featureFlagKey}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.feature_flags.copy_flag_settings`<a id="launchdarklyfeature_flagscopy_flag_settings"></a>


> ### Copying flag settings is an Enterprise feature
>
> Copying flag settings is available to customers on an Enterprise plan. To learn more, [read about our pricing](https://launchdarkly.com/pricing/). To upgrade your plan, [contact Sales](https://launchdarkly.com/contact-sales/).

Copy flag settings from a source environment to a target environment.

By default, this operation copies the entire flag configuration. You can use the `includedActions` or `excludedActions` to specify that only part of the flag configuration is copied.

If you provide the optional `currentVersion` of a flag, this operation tests to ensure that the current flag version in the environment matches the version you've specified. The operation rejects attempts to copy flag settings if the environment's current version  of the flag does not match the version you've specified. You can use this to enforce optimistic locking on copy attempts.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
copy_flag_settings_response = launchdarkly.feature_flags.copy_flag_settings(
    source={
        "key": "key_example",
    },
    target={
        "key": "key_example",
    },
    project_key="projectKey_example",
    feature_flag_key="featureFlagKey_example",
    comment="string_example",
    included_actions=["updateOn"],
    excluded_actions=["updateOn"],
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### source: [`FlagCopyConfigEnvironment`](./launch_darkly_python_sdk/type/flag_copy_config_environment.py)<a id="source-flagcopyconfigenvironmentlaunch_darkly_python_sdktypeflag_copy_config_environmentpy"></a>


##### target: [`FlagCopyConfigEnvironment`](./launch_darkly_python_sdk/type/flag_copy_config_environment.py)<a id="target-flagcopyconfigenvironmentlaunch_darkly_python_sdktypeflag_copy_config_environmentpy"></a>


##### project_key: `str`<a id="project_key-str"></a>

The project key

##### feature_flag_key: `str`<a id="feature_flag_key-str"></a>

The feature flag key. The key identifies the flag in your code.

##### comment: `str`<a id="comment-str"></a>

Optional comment

##### included_actions: [`FlagCopyConfigPostIncludedActions`](./launch_darkly_python_sdk/type/flag_copy_config_post_included_actions.py)<a id="included_actions-flagcopyconfigpostincludedactionslaunch_darkly_python_sdktypeflag_copy_config_post_included_actionspy"></a>

##### excluded_actions: [`FlagCopyConfigPostExcludedActions`](./launch_darkly_python_sdk/type/flag_copy_config_post_excluded_actions.py)<a id="excluded_actions-flagcopyconfigpostexcludedactionslaunch_darkly_python_sdktypeflag_copy_config_post_excluded_actionspy"></a>

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`FlagCopyConfigPost`](./launch_darkly_python_sdk/type/flag_copy_config_post.py)
#### 🔄 Return<a id="🔄-return"></a>

[`FeatureFlag`](./launch_darkly_python_sdk/pydantic/feature_flag.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/flags/{projectKey}/{featureFlagKey}/copy` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.feature_flags.create_feature_flag`<a id="launchdarklyfeature_flagscreate_feature_flag"></a>

Create a feature flag with the given name, key, and variations.

### Creating a migration flag<a id="creating-a-migration-flag"></a>

When you create a migration flag, the variations are pre-determined based on the number of stages in the migration.
To create a migration flag, omit the `variations` and `defaults` information. Instead, provide a `purpose` of `migration`, and `migrationSettings`. If you create a migration flag with six stages, `contextKind` is required. Otherwise, it should be omitted.

Here's an example:

```json
{
  "key": "flag-key-123",
  "purpose": "migration",
  "migrationSettings": {
    "stageCount": 6,
    "contextKind": "account"
  }
}
```

To learn more, read [Migration Flags](https://docs.launchdarkly.com/home/flag-types/migration-flags).


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
create_feature_flag_response = launchdarkly.feature_flags.create_feature_flag(
    name="My flag",
    key="flag-key-123abc",
    project_key="projectKey_example",
    tags=["example-tag"],
    description="This flag controls the example widgets",
    include_in_snippet=True,
    client_side_availability={
        "using_environment_id": True,
        "using_mobile_key": True,
    },
    variations=[{
    "value": None,
}, ],
    temporary=False,
    custom_properties={
        "key": {
            "name": "Jira issues",
            "value": ["is-123", "is-456"],
        },
    },
    defaults={
        "on_variation": 0,
        "off_variation": 1,
    },
    purpose="migration",
    migration_settings={
        "stage_count": 1,
    },
    clone="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### name: `str`<a id="name-str"></a>

A human-friendly name for the feature flag

##### key: `str`<a id="key-str"></a>

A unique key used to reference the flag in your code

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### tags: [`FeatureFlagBodyTags`](./launch_darkly_python_sdk/type/feature_flag_body_tags.py)<a id="tags-featureflagbodytagslaunch_darkly_python_sdktypefeature_flag_body_tagspy"></a>

##### description: `str`<a id="description-str"></a>

Description of the feature flag. Defaults to an empty string.

##### include_in_snippet: `bool`<a id="include_in_snippet-bool"></a>

Deprecated, use <code>clientSideAvailability</code>. Whether this flag should be made available to the client-side JavaScript SDK. Defaults to <code>false</code>.

##### client_side_availability: [`ClientSideAvailabilityPost`](./launch_darkly_python_sdk/type/client_side_availability_post.py)<a id="client_side_availability-clientsideavailabilitypostlaunch_darkly_python_sdktypeclient_side_availability_postpy"></a>


##### variations: List[`Variation`]<a id="variations-listvariation"></a>

An array of possible variations for the flag. The variation values must be unique. If omitted, two boolean variations of <code>true</code> and <code>false</code> will be used.

##### temporary: `bool`<a id="temporary-bool"></a>

Whether the flag is a temporary flag. Defaults to <code>true</code>.

##### custom_properties: [`CustomProperties`](./launch_darkly_python_sdk/type/custom_properties.py)<a id="custom_properties-custompropertieslaunch_darkly_python_sdktypecustom_propertiespy"></a>

##### defaults: [`Defaults`](./launch_darkly_python_sdk/type/defaults.py)<a id="defaults-defaultslaunch_darkly_python_sdktypedefaultspy"></a>


##### purpose: `str`<a id="purpose-str"></a>

Purpose of the flag

##### migration_settings: [`MigrationSettingsPost`](./launch_darkly_python_sdk/type/migration_settings_post.py)<a id="migration_settings-migrationsettingspostlaunch_darkly_python_sdktypemigration_settings_postpy"></a>


##### clone: `str`<a id="clone-str"></a>

The key of the feature flag to be cloned. The key identifies the flag in your code. For example, setting `clone=flagKey` copies the full targeting configuration for all environments, including `on/off` state, from the original flag to the new flag.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`FeatureFlagBody`](./launch_darkly_python_sdk/type/feature_flag_body.py)
#### 🔄 Return<a id="🔄-return"></a>

[`FeatureFlag`](./launch_darkly_python_sdk/pydantic/feature_flag.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/flags/{projectKey}` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.feature_flags.delete_flag`<a id="launchdarklyfeature_flagsdelete_flag"></a>

Delete a feature flag in all environments. Use with caution: only delete feature flags your application no longer uses.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
launchdarkly.feature_flags.delete_flag(
    project_key="projectKey_example",
    feature_flag_key="featureFlagKey_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### feature_flag_key: `str`<a id="feature_flag_key-str"></a>

The feature flag key. The key identifies the flag in your code.

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/flags/{projectKey}/{featureFlagKey}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.feature_flags.get_context_instance_segments_membership_by_env`<a id="launchdarklyfeature_flagsget_context_instance_segments_membership_by_env"></a>

Get a list of context targets on a feature flag that are scheduled for removal.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_context_instance_segments_membership_by_env_response = launchdarkly.feature_flags.get_context_instance_segments_membership_by_env(
    project_key="projectKey_example",
    environment_key="environmentKey_example",
    feature_flag_key="featureFlagKey_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

##### feature_flag_key: `str`<a id="feature_flag_key-str"></a>

The feature flag key

#### 🔄 Return<a id="🔄-return"></a>

[`ExpiringTargetGetResponse`](./launch_darkly_python_sdk/pydantic/expiring_target_get_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/flags/{projectKey}/{featureFlagKey}/expiring-targets/{environmentKey}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.feature_flags.get_status`<a id="launchdarklyfeature_flagsget_status"></a>

Get the status for a particular feature flag.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_status_response = launchdarkly.feature_flags.get_status(
    project_key="projectKey_example",
    environment_key="environmentKey_example",
    feature_flag_key="featureFlagKey_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

##### feature_flag_key: `str`<a id="feature_flag_key-str"></a>

The feature flag key

#### 🔄 Return<a id="🔄-return"></a>

[`FlagStatusRep`](./launch_darkly_python_sdk/pydantic/flag_status_rep.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/flag-statuses/{projectKey}/{environmentKey}/{featureFlagKey}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.feature_flags.list`<a id="launchdarklyfeature_flagslist"></a>

Get a list of all feature flags in the given project. By default, each flag includes configurations for each environment. You can filter environments with the `env` query parameter. For example, setting `env=production` restricts the returned configurations to just your production environment. You can also filter feature flags by tag with the `tag` query parameter.

> #### Recommended use
>
> This endpoint can return a large amount of information. We recommend using some or all of these query parameters to decrease response time and overall payload size: `limit`, `env`, `query`, and `filter=creationDate`.

### Filtering flags<a id="filtering-flags"></a>

You can filter on certain fields using the `filter` query parameter. For example, setting `filter=query:dark-mode,tags:beta+test` matches flags with the string `dark-mode` in their key or name, ignoring case, which also have the tags `beta` and `test`.

The `filter` query parameter supports the following arguments:

| Filter argument       | Description | Example              |
|-----------------------|-------------|----------------------|
| `archived`              | A boolean value. It filters the list to archived flags. Setting the value to `true` returns only archived flags. When this is absent, only unarchived flags are returned. | `filter=archived:true` |
| `contextKindsEvaluated` | A `+`-separated list of context kind keys. It filters the list to flags which have been evaluated in the past 30 days for all of the context kinds in the list. | `filter=contextKindsEvaluated:user+application` |
| `contextKindTargeted`   | A string. It filters the list to flags that are targeting the given context kind key. | `filter=contextKindTargeted:user` |
| `codeReferences.max`    | An integer value. Use `0` to return flags that do not have code references. | `filter=codeReferences.max:0` |
| `codeReferences.min`    | An integer value. Use `1` to return flags that do have code references. | `filter=codeReferences.min:1` |
| `creationDate`          | An object with an optional `before` field whose value is Unix time in milliseconds. It filters the list to flags created before the date. | `filter=creationDate:{"before":1690527600000}` |
| `evaluated`             | An object that contains a key of `after` and a value in Unix time in milliseconds. It filters the list to all flags that have been evaluated since the time you specify, in the environment provided. This filter requires the `filterEnv` filter. | `filter=evaluation:{"after":1690527600000}` |
| `filterEnv`             | A string with the key of a valid environment. You must use this field for filters that are environment-specific. If there are multiple environment-specific filters, you only need to include this field once. | `filter=evaluated:{"after": 1590768455282},filterEnv:production,status:active` |
| `followerId`            | A valid member ID. It filters the list to flags that are being followed by this member. |  `filter=followerId:12ab3c45de678910abc12345` |
| `hasDataExport`         | A boolean value. It filters the list to flags that are exporting data in the specified environment. This includes flags that are exporting data from Experimentation. This filter requires the `filterEnv` filter. | `filter=hasDataExport:true,filterEnv:production` |
| `hasExperiment`         | A boolean value. It filters the list to flags that are used in an experiment. | `filter=hasExperiment:true` |
| `maintainerId`          | A valid member ID. It filters the list to flags that are maintained by this member. | `filter=maintainerId:12ab3c45de678910abc12345` |
| `maintainerTeamKey`     | A string. It filters the list to flags that are maintained by the team with this key. | `filter=maintainerTeamKey:example-team-key` |
| `query`                 | A string. It filters the list to flags that include the specified string in their key or name. It is not case sensitive. | `filter=query:example` |
| `sdkAvailability`       | A string, one of `client`, `mobile`, `anyClient`, `server`. Using `client` filters the list to flags whose client-side SDK availability is set to use the client-side ID. Using `mobile` filters to flags set to use the mobile key. Using `anyClient` filters to flags set to use either the client-side ID or the mobile key. Using `server` filters to flags set to use neither, that is, to flags only available in server-side SDKs.  | `filter=sdkAvailability:client` |
| `segmentTargeted`       | A string. It filters the list to flags that target the segment with this key. This filter requires the `filterEnv` filter. | `filter=segmentTargeted:example-segment-key,filterEnv:production` |
| `status`                | A string, either `new`, `inactive`, `active`, or `launched`. It filters the list to flags with the specified status in the specified environment. This filter requires the `filterEnv` filter. | `filter=status:active,filterEnv:production` |
| `tags`                  | A `+`-separated list of tags. It filters the list to flags that have all of the tags in the list. | `filter=tags:beta+test` |
| `type`                  | A string, either `temporary` or `permanent`. It filters the list to flags with the specified type. | `filter=type:permanent` |

The documented values for the `filter` query are prior to URL encoding. For example, the `+` in `filter=tags:beta+test` must be encoded to `%2B`.

By default, this endpoint returns all flags. You can page through the list with the `limit` parameter and by following the `first`, `prev`, `next`, and `last` links in the returned `_links` field. These links will not be present if the pages they refer to don't exist. For example, the `first` and `prev` links will be missing from the response on the first page.

### Sorting flags<a id="sorting-flags"></a>

You can sort flags based on the following fields:

- `creationDate` sorts by the creation date of the flag.
- `key` sorts by the key of the flag.
- `maintainerId` sorts by the flag maintainer.
- `name` sorts by flag name.
- `tags` sorts by tags.
- `targetingModifiedDate` sorts by the date that the flag's targeting rules were last modified in a given environment. It must be used with `env` parameter and it can not be combined with any other sort. If multiple `env` values are provided, it will perform sort using the first one. For example, `sort=-targetingModifiedDate&env=production&env=staging` returns results sorted by `targetingModifiedDate` for the `production` environment.
- `type` sorts by flag type

All fields are sorted in ascending order by default. To sort in descending order, prefix the field with a dash ( - ). For example, `sort=-name` sorts the response by flag name in descending order.

### Expanding response<a id="expanding-response"></a>

LaunchDarkly supports the `expand` query param to include additional fields in the response, with the following fields:

- `codeReferences` includes code references for the feature flag
- `evaluation` includes evaluation information within returned environments, including which context kinds the flag has been evaluated for in the past 30 days
- `migrationSettings` includes migration settings information within the flag and within returned environments. These settings are only included for migration flags, that is, where `purpose` is `migration`.

For example, `expand=evaluation` includes the `evaluation` field in the response.

### Migration flags<a id="migration-flags"></a>
For migration flags, the cohort information is included in the `rules` property of a flag's response, and default cohort information is included in the `fallthrough` property of a flag's response.
To learn more, read [Migration Flags](https://docs.launchdarkly.com/home/flag-types/migration-flags).


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_response = launchdarkly.feature_flags.list(
    project_key="projectKey_example",
    env="string_example",
    tag="string_example",
    limit=1,
    offset=1,
    archived=True,
    summary=True,
    filter="string_example",
    sort="string_example",
    compare=True,
    expand="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### env: `str`<a id="env-str"></a>

Filter configurations by environment

##### tag: `str`<a id="tag-str"></a>

Filter feature flags by tag

##### limit: `int`<a id="limit-int"></a>

The number of feature flags to return. Defaults to -1, which returns all flags

##### offset: `int`<a id="offset-int"></a>

Where to start in the list. Use this with pagination. For example, an offset of 10 skips the first ten items and then returns the next items in the list, up to the query `limit`.

##### archived: `bool`<a id="archived-bool"></a>

Deprecated, use `filter=archived:true` instead. A boolean to filter the list to archived flags. When this is absent, only unarchived flags will be returned

##### summary: `bool`<a id="summary-bool"></a>

By default, flags do _not_ include their lists of prerequisites, targets, or rules for each environment. Set `summary=0` to include these fields for each flag returned.

##### filter: `str`<a id="filter-str"></a>

A comma-separated list of filters. Each filter is of the form field:value. Read the endpoint description for a full list of available filter fields.

##### sort: `str`<a id="sort-str"></a>

A comma-separated list of fields to sort by. Fields prefixed by a dash ( - ) sort in descending order. Read the endpoint description for a full list of available sort fields.

##### compare: `bool`<a id="compare-bool"></a>

A boolean to filter results by only flags that have differences between environments

##### expand: `str`<a id="expand-str"></a>

A comma-separated list of fields to expand in the response. Supported fields are explained above.

#### 🔄 Return<a id="🔄-return"></a>

[`FeatureFlags`](./launch_darkly_python_sdk/pydantic/feature_flags.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/flags/{projectKey}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.feature_flags.list_expiring_user_targets`<a id="launchdarklyfeature_flagslist_expiring_user_targets"></a>


> ### Contexts are now available
>
> After you have upgraded your LaunchDarkly SDK to use contexts instead of users, you should use [Get expiring context targets for feature flag](https://apidocs.launchdarkly.com) instead of this endpoint. To learn more, read [Contexts](https://docs.launchdarkly.com/home/contexts).

Get a list of user targets on a feature flag that are scheduled for removal.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_expiring_user_targets_response = launchdarkly.feature_flags.list_expiring_user_targets(
    project_key="projectKey_example",
    environment_key="environmentKey_example",
    feature_flag_key="featureFlagKey_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

##### feature_flag_key: `str`<a id="feature_flag_key-str"></a>

The feature flag key

#### 🔄 Return<a id="🔄-return"></a>

[`ExpiringUserTargetGetResponse`](./launch_darkly_python_sdk/pydantic/expiring_user_target_get_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/flags/{projectKey}/{featureFlagKey}/expiring-user-targets/{environmentKey}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.feature_flags.list_flag_statuses`<a id="launchdarklyfeature_flagslist_flag_statuses"></a>

Get a list of statuses for all feature flags. The status includes the last time the feature flag was requested, as well as a state, which is one of the following:

- `new`: You created the flag fewer than seven days ago and it has never been requested.
- `active`: LaunchDarkly is receiving requests for this flag, but there are either multiple variations configured, or it is toggled off, or there have been changes to configuration in the past seven days.
- `inactive`: You created the feature flag more than seven days ago, and hasn't been requested within the past seven days.
- `launched`: LaunchDarkly is receiving requests for this flag, it is toggled on, there is only one variation configured, and there have been no changes to configuration in the past seven days.

To learn more, read [Flag statuses](https://docs.launchdarkly.com/home/code/flag-status).


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_flag_statuses_response = launchdarkly.feature_flags.list_flag_statuses(
    project_key="projectKey_example",
    environment_key="environmentKey_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

#### 🔄 Return<a id="🔄-return"></a>

[`FeatureFlagStatuses`](./launch_darkly_python_sdk/pydantic/feature_flag_statuses.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/flag-statuses/{projectKey}/{environmentKey}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.feature_flags.single_flag_by_key`<a id="launchdarklyfeature_flagssingle_flag_by_key"></a>

Get a single feature flag by key. By default, this returns the configurations for all environments. You can filter environments with the `env` query parameter. For example, setting `env=production` restricts the returned configurations to just the `production` environment.

> #### Recommended use
>
> This endpoint can return a large amount of information. Specifying one or multiple environments with the `env` parameter can decrease response time and overall payload size. We recommend using this parameter to return only the environments relevant to your query.

### Expanding response<a id="expanding-response"></a>

LaunchDarkly supports the `expand` query param to include additional fields in the response, with the following fields:

- `evaluation` includes evaluation information within returned environments, including which context kinds the flag has been evaluated for in the past 30 days 
- `migrationSettings` includes migration settings information within the flag and within returned environments. These settings are only included for migration flags, that is, where `purpose` is `migration`.

For example, `expand=evaluation` includes the `evaluation` field in the response.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
single_flag_by_key_response = launchdarkly.feature_flags.single_flag_by_key(
    project_key="projectKey_example",
    feature_flag_key="featureFlagKey_example",
    env="string_example",
    expand="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### feature_flag_key: `str`<a id="feature_flag_key-str"></a>

The feature flag key

##### env: `str`<a id="env-str"></a>

Filter configurations by environment

##### expand: `str`<a id="expand-str"></a>

A comma-separated list of fields to expand in the response. Supported fields are explained above.

#### 🔄 Return<a id="🔄-return"></a>

[`FeatureFlag`](./launch_darkly_python_sdk/pydantic/feature_flag.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/flags/{projectKey}/{featureFlagKey}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.feature_flags.update_expiring_context_targets`<a id="launchdarklyfeature_flagsupdate_expiring_context_targets"></a>

Schedule a context for removal from individual targeting on a feature flag. The flag must already individually target the context.

You can add, update, or remove a scheduled removal date. You can only schedule a context for removal on a single variation per flag.

Updating an expiring target uses the semantic patch format. To make a semantic patch request, you must append `domain-model=launchdarkly.semanticpatch` to your `Content-Type` header. To learn more, read [Updates using semantic patch](https://apidocs.launchdarkly.com).

### Instructions<a id="instructions"></a>

Semantic patch requests support the following `kind` instructions for updating expiring targets.

<details>
<summary>Click to expand instructions for <strong>updating expiring targets</strong></summary>

#### addExpiringTarget<a id="addexpiringtarget"></a>

Adds a date and time that LaunchDarkly will remove the context from the flag's individual targeting.

##### Parameters<a id="parameters"></a>

* `value`: The time, in Unix milliseconds, when LaunchDarkly should remove the context from individual targeting for this flag
* `variationId`: ID of a variation on the flag
* `contextKey`: The context key for the context to remove from individual targeting
* `contextKind`: The kind of context represented by the `contextKey`

Here's an example:

```json
{
  "instructions": [{
    "kind": "addExpiringTarget",
    "value": 1754006460000,
    "variationId": "4254742c-71ae-411f-a992-43b18a51afe0",
    "contextKey": "user-key-123abc",
    "contextKind": "user"
  }]
}
```

#### updateExpiringTarget<a id="updateexpiringtarget"></a>

Updates the date and time that LaunchDarkly will remove the context from the flag's individual targeting

##### Parameters<a id="parameters"></a>

* `value`: The time, in Unix milliseconds, when LaunchDarkly should remove the context from individual targeting for this flag
* `variationId`: ID of a variation on the flag
* `contextKey`: The context key for the context to remove from individual targeting
* `contextKind`: The kind of context represented by the `contextKey`
* `version`: (Optional) The version of the expiring target to update. If included, update will fail if version doesn't match current version of the expiring target.

Here's an example:

```json
{
  "instructions": [{
    "kind": "updateExpiringTarget",
    "value": 1754006460000,
    "variationId": "4254742c-71ae-411f-a992-43b18a51afe0",
    "contextKey": "user-key-123abc",
    "contextKind": "user"
  }]
}
```

#### removeExpiringTarget<a id="removeexpiringtarget"></a>

Removes the scheduled removal of the context from the flag's individual targeting. The context will remain part of the flag's individual targeting until you explicitly remove it, or until you schedule another removal.

##### Parameters<a id="parameters"></a>

* `variationId`: ID of a variation on the flag
* `contextKey`: The context key for the context to remove from individual targeting
* `contextKind`: The kind of context represented by the `contextKey`

Here's an example:

```json
{
  "instructions": [{
    "kind": "removeExpiringTarget",
    "variationId": "4254742c-71ae-411f-a992-43b18a51afe0",
    "contextKey": "user-key-123abc",
    "contextKind": "user"
  }]
}
```

</details>


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
update_expiring_context_targets_response = launchdarkly.feature_flags.update_expiring_context_targets(
    instructions=[{
    "key": None,
}],
    project_key="projectKey_example",
    environment_key="environmentKey_example",
    feature_flag_key="featureFlagKey_example",
    comment="optional comment",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### instructions: List[[`Instruction`](./launch_darkly_python_sdk/type/instruction.py)]<a id="instructions-listinstructionlaunch_darkly_python_sdktypeinstructionpy"></a>

The instructions to perform when updating

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

##### feature_flag_key: `str`<a id="feature_flag_key-str"></a>

The feature flag key

##### comment: `str`<a id="comment-str"></a>

Optional comment describing the change

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`PatchFlagsRequest`](./launch_darkly_python_sdk/type/patch_flags_request.py)
#### 🔄 Return<a id="🔄-return"></a>

[`ExpiringTargetPatchResponse`](./launch_darkly_python_sdk/pydantic/expiring_target_patch_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/flags/{projectKey}/{featureFlagKey}/expiring-targets/{environmentKey}` `patch`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.feature_flags.update_expiring_user_targets`<a id="launchdarklyfeature_flagsupdate_expiring_user_targets"></a>

> ### Contexts are now available
>
> After you have upgraded your LaunchDarkly SDK to use contexts instead of users, you should use [Update expiring context targets on feature flag](https://apidocs.launchdarkly.com) instead of this endpoint. To learn more, read [Contexts](https://docs.launchdarkly.com/home/contexts).

Schedule a target for removal from individual targeting on a feature flag. The flag must already serve a variation to specific targets based on their key.

You can add, update, or remove a scheduled removal date. You can only schedule a target for removal on a single variation per flag.

Updating an expiring target uses the semantic patch format. To make a semantic patch request, you must append `domain-model=launchdarkly.semanticpatch` to your `Content-Type` header. To learn more, read [Updates using semantic patch](https://apidocs.launchdarkly.com).

### Instructions<a id="instructions"></a>

Semantic patch requests support the following `kind` instructions for updating expiring user targets.

<details>
<summary>Click to expand instructions for <strong>updating expiring user targets</strong></summary>

#### addExpireUserTargetDate<a id="addexpireusertargetdate"></a>

Adds a date and time that LaunchDarkly will remove the user from the flag's individual targeting.

##### Parameters<a id="parameters"></a>

* `value`: The time, in Unix milliseconds, when LaunchDarkly should remove the user from individual targeting for this flag
* `variationId`: ID of a variation on the flag
* `userKey`: The user key for the user to remove from individual targeting

#### updateExpireUserTargetDate<a id="updateexpireusertargetdate"></a>

Updates the date and time that LaunchDarkly will remove the user from the flag's individual targeting.

##### Parameters<a id="parameters"></a>

* `value`: The time, in Unix milliseconds, when LaunchDarkly should remove the user from individual targeting for this flag
* `variationId`: ID of a variation on the flag
* `userKey`: The user key for the user to remove from individual targeting
* `version`: (Optional) The version of the expiring user target to update. If included, update will fail if version doesn't match current version of the expiring user target.

#### removeExpireUserTargetDate<a id="removeexpireusertargetdate"></a>

Removes the scheduled removal of the user from the flag's individual targeting. The user will remain part of the flag's individual targeting until you explicitly remove them, or until you schedule another removal.

##### Parameters<a id="parameters"></a>

* `variationId`: ID of a variation on the flag
* `userKey`: The user key for the user to remove from individual targeting

</details>


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
update_expiring_user_targets_response = launchdarkly.feature_flags.update_expiring_user_targets(
    instructions=[{
    "key": None,
}],
    project_key="projectKey_example",
    environment_key="environmentKey_example",
    feature_flag_key="featureFlagKey_example",
    comment="optional comment",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### instructions: List[[`Instruction`](./launch_darkly_python_sdk/type/instruction.py)]<a id="instructions-listinstructionlaunch_darkly_python_sdktypeinstructionpy"></a>

The instructions to perform when updating

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

##### feature_flag_key: `str`<a id="feature_flag_key-str"></a>

The feature flag key

##### comment: `str`<a id="comment-str"></a>

Optional comment describing the change

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`PatchFlagsRequest`](./launch_darkly_python_sdk/type/patch_flags_request.py)
#### 🔄 Return<a id="🔄-return"></a>

[`ExpiringUserTargetPatchResponse`](./launch_darkly_python_sdk/pydantic/expiring_user_target_patch_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/flags/{projectKey}/{featureFlagKey}/expiring-user-targets/{environmentKey}` `patch`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.feature_flags.update_feature_flag`<a id="launchdarklyfeature_flagsupdate_feature_flag"></a>

Perform a partial update to a feature flag. The request body must be a valid semantic patch, JSON patch, or JSON merge patch. To learn more the different formats, read [Updates](https://apidocs.launchdarkly.com).

### Using semantic patches on a feature flag<a id="using-semantic-patches-on-a-feature-flag"></a>

To make a semantic patch request, you must append `domain-model=launchdarkly.semanticpatch` to your `Content-Type` header. To learn more, read [Updates using semantic patch](https://apidocs.launchdarkly.com).

The body of a semantic patch request for updating feature flags takes the following properties:

* `comment` (string): (Optional) A description of the update.
* `environmentKey` (string): (Required for some instructions only) The key of the LaunchDarkly environment.
* `instructions` (array): (Required) A list of actions the update should perform. Each action in the list must be an object with a `kind` property that indicates the instruction. If the action requires parameters, you must include those parameters as additional fields in the object. The body of a single semantic patch can contain many different instructions.

### Instructions<a id="instructions"></a>

Semantic patch requests support the following `kind` instructions for updating feature flags.

<details>
<summary>Click to expand instructions for <strong>turning flags on and off</strong></summary>

These instructions require the `environmentKey` parameter.

#### turnFlagOff<a id="turnflagoff"></a>

Sets the flag's targeting state to **Off**.

Here's an example:

```json
{
  "environmentKey": "environment-key-123abc",
  "instructions": [ { "kind": "turnFlagOff" } ]
}
```

#### turnFlagOn<a id="turnflagon"></a>

Sets the flag's targeting state to **On**.

Here's an example:

```json
{
  "environmentKey": "environment-key-123abc",
  "instructions": [ { "kind": "turnFlagOn" } ]
}
```

</details><br />

<details>
<summary>Click to expand instructions for <strong>working with targeting and variations</strong></summary>

These instructions require the `environmentKey` parameter.

Several of the instructions for working with targeting and variations require flag rule IDs, variation IDs, or clause IDs as parameters. Each of these are returned as part of the [Get feature flag](https://apidocs.launchdarkly.com) response. The flag rule ID is the `_id` field of each element in the `rules` array within each environment listed in the `environments` object. The variation ID is the `_id` field in each element of the `variations` array. The clause ID is the `_id` field of each element of the `clauses` array within the `rules` array within each environment listed in the `environments` object.

#### addClauses<a id="addclauses"></a>

Adds the given clauses to the rule indicated by `ruleId`.

##### Parameters<a id="parameters"></a>

- `ruleId`: ID of a rule in the flag.
- `clauses`: Array of clause objects, with `contextKind` (string), `attribute` (string), `op` (string), `negate` (boolean), and `values` (array of strings, numbers, or dates) properties. The `contextKind`, `attribute`, and `values` are case sensitive. The `op` must be lower-case.

Here's an example:

```json
{
	"environmentKey": "environment-key-123abc",
	"instructions": [{
		"kind": "addClauses",
		"ruleId": "a902ef4a-2faf-4eaf-88e1-ecc356708a29",
		"clauses": [{
			"contextKind": "user",
			"attribute": "country",
			"op": "in",
			"negate": false,
			"values": ["USA", "Canada"]
		}]
	}]
}
```

#### addPrerequisite<a id="addprerequisite"></a>

Adds the flag indicated by `key` with variation `variationId` as a prerequisite to the flag in the path parameter.

##### Parameters<a id="parameters"></a>

- `key`: Flag key of the prerequisite flag.
- `variationId`: ID of a variation of the prerequisite flag.

Here's an example:

```json
{
	"environmentKey": "environment-key-123abc",
	"instructions": [{
		"kind": "addPrerequisite",
		"key": "example-prereq-flag-key",
		"variationId": "2f43f67c-3e4e-4945-a18a-26559378ca00"
	}]
}
```

#### addRule<a id="addrule"></a>

Adds a new targeting rule to the flag. The rule may contain `clauses` and serve the variation that `variationId` indicates, or serve a percentage rollout that `rolloutWeights`, `rolloutBucketBy`, and `rolloutContextKind` indicate.

If you set `beforeRuleId`, this adds the new rule before the indicated rule. Otherwise, adds the new rule to the end of the list.

##### Parameters<a id="parameters"></a>

- `clauses`: Array of clause objects, with `contextKind` (string), `attribute` (string), `op` (string), `negate` (boolean), and `values` (array of strings, numbers, or dates) properties. The `contextKind`, `attribute`, and `values` are case sensitive. The `op` must be lower-case.
- `beforeRuleId`: (Optional) ID of a flag rule.
- Either
  - `variationId`: ID of a variation of the flag.

  or

  - `rolloutWeights`: (Optional) Map of `variationId` to weight, in thousandths of a percent (0-100000).
  - `rolloutBucketBy`: (Optional) Context attribute available in the specified `rolloutContextKind`.
  - `rolloutContextKind`: (Optional) Context kind, defaults to `user`

Here's an example that uses a `variationId`:

```json
{
  "environmentKey": "environment-key-123abc",
  "instructions": [{
    "kind": "addRule",
    "variationId": "2f43f67c-3e4e-4945-a18a-26559378ca00",
    "clauses": [{
      "contextKind": "organization",
      "attribute": "located_in",
      "op": "in",
      "negate": false,
      "values": ["Sweden", "Norway"]
    }]
  }]
}
```

Here's an example that uses a percentage rollout:

```json
{
  "environmentKey": "environment-key-123abc",
  "instructions": [{
    "kind": "addRule",
    "clauses": [{
      "contextKind": "organization",
      "attribute": "located_in",
      "op": "in",
      "negate": false,
      "values": ["Sweden", "Norway"]
    }],
    "rolloutContextKind": "organization",
    "rolloutWeights": {
      "2f43f67c-3e4e-4945-a18a-26559378ca00": 15000, // serve 15% this variation
      "e5830889-1ec5-4b0c-9cc9-c48790090c43": 85000  // serve 85% this variation
    }
  }]
}
```

#### addTargets<a id="addtargets"></a>

Adds context keys to the individual context targets for the context kind that `contextKind` specifies and the variation that `variationId` specifies. Returns an error if this causes the flag to target the same context key in multiple variations.

##### Parameters<a id="parameters"></a>

- `values`: List of context keys.
- `contextKind`: (Optional) Context kind to target, defaults to `user`
- `variationId`: ID of a variation on the flag.

Here's an example:

```json
{
	"environmentKey": "environment-key-123abc",
	"instructions": [{
		"kind": "addTargets",
		"values": ["context-key-123abc", "context-key-456def"],
		"variationId": "2f43f67c-3e4e-4945-a18a-26559378ca00"
	}]
}
```

#### addUserTargets<a id="addusertargets"></a>

Adds user keys to the individual user targets for the variation that `variationId` specifies. Returns an error if this causes the flag to target the same user key in multiple variations. If you are working with contexts, use `addTargets` instead of this instruction.

##### Parameters<a id="parameters"></a>

- `values`: List of user keys.
- `variationId`: ID of a variation on the flag.

Here's an example:

```json
{
	"environmentKey": "environment-key-123abc",
	"instructions": [{
		"kind": "addUserTargets",
		"values": ["user-key-123abc", "user-key-456def"],
		"variationId": "2f43f67c-3e4e-4945-a18a-26559378ca00"
	}]
}
```

#### addValuesToClause<a id="addvaluestoclause"></a>

Adds `values` to the values of the clause that `ruleId` and `clauseId` indicate. Does not update the context kind, attribute, or operator.

##### Parameters<a id="parameters"></a>

- `ruleId`: ID of a rule in the flag.
- `clauseId`: ID of a clause in that rule.
- `values`: Array of strings, case sensitive.

Here's an example:

```json
{
	"environmentKey": "environment-key-123abc",
	"instructions": [{
		"kind": "addValuesToClause",
		"ruleId": "a902ef4a-2faf-4eaf-88e1-ecc356708a29",
		"clauseId": "10a58772-3121-400f-846b-b8a04e8944ed",
		"values": ["beta_testers"]
	}]
}
```

#### addVariation<a id="addvariation"></a>

Adds a variation to the flag.

##### Parameters<a id="parameters"></a>

- `value`: The variation value.
- `name`: (Optional) The variation name.
- `description`: (Optional) A description for the variation.

Here's an example:

```json
{
	"instructions": [ { "kind": "addVariation", "value": 20, "name": "New variation" } ]
}
```

#### clearTargets<a id="cleartargets"></a>

Removes all individual targets from the variation that `variationId` specifies. This includes both user and non-user targets.

##### Parameters<a id="parameters"></a>

- `variationId`: ID of a variation on the flag.

Here's an example:

```json
{
  "environmentKey": "environment-key-123abc",
  "instructions": [ { "kind": "clearTargets", "variationId": "2f43f67c-3e4e-4945-a18a-26559378ca00" } ]
}
```

#### clearUserTargets<a id="clearusertargets"></a>

Removes all individual user targets from the variation that `variationId` specifies. If you are working with contexts, use `clearTargets` instead of this instruction.

##### Parameters<a id="parameters"></a>

- `variationId`: ID of a variation on the flag.

Here's an example:

```json
{
  "environmentKey": "environment-key-123abc",
  "instructions": [ { "kind": "clearUserTargets", "variationId": "2f43f67c-3e4e-4945-a18a-26559378ca00" } ]
}
```

#### removeClauses<a id="removeclauses"></a>

Removes the clauses specified by `clauseIds` from the rule indicated by `ruleId`.

##### Parameters<a id="parameters"></a>

- `ruleId`: ID of a rule in the flag.
- `clauseIds`: Array of IDs of clauses in the rule.

Here's an example:

```json
{
	"environmentKey": "environment-key-123abc",
	"instructions": [{
		"kind": "removeClauses",
		"ruleId": "a902ef4a-2faf-4eaf-88e1-ecc356708a29",
		"clauseIds": ["10a58772-3121-400f-846b-b8a04e8944ed", "36a461dc-235e-4b08-97b9-73ce9365873e"]
	}]
}
```

#### removePrerequisite<a id="removeprerequisite"></a>

Removes the prerequisite flag indicated by `key`. Does nothing if this prerequisite does not exist.

##### Parameters<a id="parameters"></a>

- `key`: Flag key of an existing prerequisite flag.

Here's an example:

```json
{
  "environmentKey": "environment-key-123abc",
  "instructions": [ { "kind": "removePrerequisite", "key": "prereq-flag-key-123abc" } ]
}
```

#### removeRule<a id="removerule"></a>

Removes the targeting rule specified by `ruleId`. Does nothing if the rule does not exist.

##### Parameters<a id="parameters"></a>

- `ruleId`: ID of a rule in the flag.

Here's an example:

```json
{
  "environmentKey": "environment-key-123abc",
  "instructions": [ { "kind": "removeRule", "ruleId": "a902ef4a-2faf-4eaf-88e1-ecc356708a29" } ]
}
```

#### removeTargets<a id="removetargets"></a>

Removes context keys from the individual context targets for the context kind that `contextKind` specifies and the variation that `variationId` specifies. Does nothing if the flag does not target the context keys.

##### Parameters<a id="parameters"></a>

- `values`: List of context keys.
- `contextKind`: (Optional) Context kind to target, defaults to `user`
- `variationId`: ID of a flag variation.

Here's an example:

```json
{
	"environmentKey": "environment-key-123abc",
	"instructions": [{
		"kind": "removeTargets",
		"values": ["context-key-123abc", "context-key-456def"],
		"variationId": "2f43f67c-3e4e-4945-a18a-26559378ca00"
	}]
}
```

#### removeUserTargets<a id="removeusertargets"></a>

Removes user keys from the individual user targets for the variation that `variationId` specifies. Does nothing if the flag does not target the user keys. If you are working with contexts, use `removeTargets` instead of this instruction.

##### Parameters<a id="parameters"></a>

- `values`: List of user keys.
- `variationId`: ID of a flag variation.

Here's an example:

```json
{
	"environmentKey": "environment-key-123abc",
	"instructions": [{
		"kind": "removeUserTargets",
		"values": ["user-key-123abc", "user-key-456def"],
		"variationId": "2f43f67c-3e4e-4945-a18a-26559378ca00"
	}]
}
```

#### removeValuesFromClause<a id="removevaluesfromclause"></a>

Removes `values` from the values of the clause indicated by `ruleId` and `clauseId`. Does not update the context kind, attribute, or operator.

##### Parameters<a id="parameters"></a>

- `ruleId`: ID of a rule in the flag.
- `clauseId`: ID of a clause in that rule.
- `values`: Array of strings, case sensitive.

Here's an example:

```json
{
	"environmentKey": "environment-key-123abc",
	"instructions": [{
		"kind": "removeValuesFromClause",
		"ruleId": "a902ef4a-2faf-4eaf-88e1-ecc356708a29",
		"clauseId": "10a58772-3121-400f-846b-b8a04e8944ed",
		"values": ["beta_testers"]
	}]
}
```

#### removeVariation<a id="removevariation"></a>

Removes a variation from the flag.

##### Parameters<a id="parameters"></a>

- `variationId`: ID of a variation of the flag to remove.

Here's an example:

```json
{
	"instructions": [ { "kind": "removeVariation", "variationId": "2f43f67c-3e4e-4945-a18a-26559378ca00" } ]
}
```

#### reorderRules<a id="reorderrules"></a>

Rearranges the rules to match the order given in `ruleIds`. Returns an error if `ruleIds` does not match the current set of rules on the flag.

##### Parameters<a id="parameters"></a>

- `ruleIds`: Array of IDs of all rules in the flag.

Here's an example:

```json
{
	"environmentKey": "environment-key-123abc",
	"instructions": [{
		"kind": "reorderRules",
		"ruleIds": ["a902ef4a-2faf-4eaf-88e1-ecc356708a29", "63c238d1-835d-435e-8f21-c8d5e40b2a3d"]
	}]
}
```

#### replacePrerequisites<a id="replaceprerequisites"></a>

Removes all existing prerequisites and replaces them with the list you provide.

##### Parameters<a id="parameters"></a>

- `prerequisites`: A list of prerequisites. Each item in the list must include a flag `key` and `variationId`.

Here's an example:

```json
{
  "environmentKey": "environment-key-123abc",
  "instructions": [
    {
      "kind": "replacePrerequisites",
      "prerequisites": [
        {
          "key": "prereq-flag-key-123abc",
          "variationId": "10a58772-3121-400f-846b-b8a04e8944ed"
        },
        {
          "key": "another-prereq-flag-key-456def",
          "variationId": "e5830889-1ec5-4b0c-9cc9-c48790090c43"
        }
      ]
    }
  ]
}
```

#### replaceRules<a id="replacerules"></a>

Removes all targeting rules for the flag and replaces them with the list you provide.

##### Parameters<a id="parameters"></a>

- `rules`: A list of rules.

Here's an example:

```json
{
  "environmentKey": "environment-key-123abc",
  "instructions": [
    {
      "kind": "replaceRules",
      "rules": [
        {
          "variationId": "2f43f67c-3e4e-4945-a18a-26559378ca00",
          "description": "My new rule",
          "clauses": [
            {
              "contextKind": "user",
              "attribute": "segmentMatch",
              "op": "segmentMatch",
              "values": ["test"]
            }
          ],
          "trackEvents": true
        }
      ]
    }
  ]
}
```

#### replaceTargets<a id="replacetargets"></a>

Removes all existing targeting and replaces it with the list of targets you provide.

##### Parameters<a id="parameters"></a>

- `targets`: A list of context targeting. Each item in the list includes an optional `contextKind` that defaults to `user`, a required `variationId`, and a required list of `values`.

Here's an example:

```json
{
  "environmentKey": "environment-key-123abc",
  "instructions": [
    {
      "kind": "replaceTargets",
      "targets": [
        {
          "contextKind": "user",
          "variationId": "2f43f67c-3e4e-4945-a18a-26559378ca00",
          "values": ["user-key-123abc"]
        },
        {
          "contextKind": "device",
          "variationId": "e5830889-1ec5-4b0c-9cc9-c48790090c43",
          "values": ["device-key-456def"]
        }
      ]
    }    
  ]
}
```

#### replaceUserTargets<a id="replaceusertargets"></a>

Removes all existing user targeting and replaces it with the list of targets you provide. In the list of targets, you must include a target for each of the flag's variations. If you are working with contexts, use `replaceTargets` instead of this instruction.

##### Parameters<a id="parameters"></a>

- `targets`: A list of user targeting. Each item in the list must include a `variationId` and a list of `values`.

Here's an example:

```json
{
  "environmentKey": "environment-key-123abc",
  "instructions": [
    {
      "kind": "replaceUserTargets",
      "targets": [
        {
          "variationId": "2f43f67c-3e4e-4945-a18a-26559378ca00",
          "values": ["user-key-123abc", "user-key-456def"]
        },
        {
          "variationId": "e5830889-1ec5-4b0c-9cc9-c48790090c43",
          "values": ["user-key-789ghi"]
        }
      ]
    }
  ]
}
```

#### updateClause<a id="updateclause"></a>

Replaces the clause indicated by `ruleId` and `clauseId` with `clause`.

##### Parameters<a id="parameters"></a>

- `ruleId`: ID of a rule in the flag.
- `clauseId`: ID of a clause in that rule.
- `clause`: New `clause` object, with `contextKind` (string), `attribute` (string), `op` (string), `negate` (boolean), and `values` (array of strings, numbers, or dates) properties. The `contextKind`, `attribute`, and `values` are case sensitive. The `op` must be lower-case.

Here's an example:

```json
{
  "environmentKey": "environment-key-123abc",
  "instructions": [{
    "kind": "updateClause",
    "ruleId": "a902ef4a-2faf-4eaf-88e1-ecc356708a29",
    "clauseId": "10c7462a-2062-45ba-a8bb-dfb3de0f8af5",
    "clause": {
      "contextKind": "user",
      "attribute": "country",
      "op": "in",
      "negate": false,
      "values": ["Mexico", "Canada"]
    }
  }]
}
```

#### updateDefaultVariation<a id="updatedefaultvariation"></a>

Updates the default on or off variation of the flag.

##### Parameters<a id="parameters"></a>

- `onVariationValue`: (Optional) The value of the variation of the new on variation.
- `offVariationValue`: (Optional) The value of the variation of the new off variation

Here's an example:

```json
{
	"instructions": [ { "kind": "updateDefaultVariation", "OnVariationValue": true, "OffVariationValue": false } ]
}
```

#### updateFallthroughVariationOrRollout<a id="updatefallthroughvariationorrollout"></a>

Updates the default or "fallthrough" rule for the flag, which the flag serves when a context matches none of the targeting rules. The rule can serve either the variation that `variationId` indicates, or a percentage rollout that `rolloutWeights` and `rolloutBucketBy` indicate.

##### Parameters<a id="parameters"></a>

- `variationId`: ID of a variation of the flag.

or

- `rolloutWeights`: Map of `variationId` to weight, in thousandths of a percent (0-100000).
- `rolloutBucketBy`: (Optional) Context attribute available in the specified `rolloutContextKind`.
- `rolloutContextKind`: (Optional) Context kind, defaults to `user`

Here's an example that uses a `variationId`:

```json
{
	"environmentKey": "environment-key-123abc",
	"instructions": [{
		"kind": "updateFallthroughVariationOrRollout",
		"variationId": "2f43f67c-3e4e-4945-a18a-26559378ca00"
	}]
}
```

Here's an example that uses a percentage rollout:

```json
{
	"environmentKey": "environment-key-123abc",
	"instructions": [{
		"kind": "updateFallthroughVariationOrRollout",
		"rolloutContextKind": "user",
		"rolloutWeights": {
			"2f43f67c-3e4e-4945-a18a-26559378ca00": 15000, // serve 15% this variation
			"e5830889-1ec5-4b0c-9cc9-c48790090c43": 85000  // serve 85% this variation
		}
	}]
}
```

#### updateOffVariation<a id="updateoffvariation"></a>

Updates the default off variation to `variationId`. The flag serves the default off variation when the flag's targeting is **Off**.

##### Parameters<a id="parameters"></a>

- `variationId`: ID of a variation of the flag.

Here's an example:

```json
{
  "environmentKey": "environment-key-123abc",
  "instructions": [ { "kind": "updateOffVariation", "variationId": "2f43f67c-3e4e-4945-a18a-26559378ca00" } ]
}
```

#### updatePrerequisite<a id="updateprerequisite"></a>

Changes the prerequisite flag that `key` indicates to use the variation that `variationId` indicates. Returns an error if this prerequisite does not exist.

##### Parameters<a id="parameters"></a>

- `key`: Flag key of an existing prerequisite flag.
- `variationId`: ID of a variation of the prerequisite flag.

Here's an example:

```json
{
	"environmentKey": "environment-key-123abc",
	"instructions": [{
		"kind": "updatePrerequisite",
		"key": "example-prereq-flag-key",
		"variationId": "2f43f67c-3e4e-4945-a18a-26559378ca00"
	}]
}
```

#### updateRuleDescription<a id="updateruledescription"></a>

Updates the description of the feature flag rule.

##### Parameters<a id="parameters"></a>

- `description`: The new human-readable description for this rule.
- `ruleId`: The ID of the rule. You can retrieve this by making a GET request for the flag.

Here's an example:

```json
{
	"environmentKey": "environment-key-123abc",
	"instructions": [{
		"kind": "updateRuleDescription",
		"description": "New rule description",
		"ruleId": "a902ef4a-2faf-4eaf-88e1-ecc356708a29"
	}]
}
```

#### updateRuleTrackEvents<a id="updateruletrackevents"></a>

Updates whether or not LaunchDarkly tracks events for the feature flag associated with this rule.

##### Parameters<a id="parameters"></a>

- `ruleId`: The ID of the rule. You can retrieve this by making a GET request for the flag.
- `trackEvents`: Whether or not events are tracked.

Here's an example:

```json
{
	"environmentKey": "environment-key-123abc",
	"instructions": [{
		"kind": "updateRuleTrackEvents",
		"ruleId": "a902ef4a-2faf-4eaf-88e1-ecc356708a29",
		"trackEvents": true
	}]
}
```

#### updateRuleVariationOrRollout<a id="updaterulevariationorrollout"></a>

Updates what `ruleId` serves when its clauses evaluate to true. The rule can serve either the variation that `variationId` indicates, or a percent rollout that `rolloutWeights` and `rolloutBucketBy` indicate.

##### Parameters<a id="parameters"></a>

- `ruleId`: ID of a rule in the flag.
- `variationId`: ID of a variation of the flag.

  or

- `rolloutWeights`: Map of `variationId` to weight, in thousandths of a percent (0-100000).
- `rolloutBucketBy`: (Optional) Context attribute available in the specified `rolloutContextKind`.
- `rolloutContextKind`: (Optional) Context kind, defaults to `user`

Here's an example:

```json
{
	"environmentKey": "environment-key-123abc",
	"instructions": [{
		"kind": "updateRuleVariationOrRollout",
		"ruleId": "a902ef4a-2faf-4eaf-88e1-ecc356708a29",
		"variationId": "2f43f67c-3e4e-4945-a18a-26559378ca00"
	}]
}
```

#### updateTrackEvents<a id="updatetrackevents"></a>

Updates whether or not LaunchDarkly tracks events for the feature flag, for all rules.

##### Parameters<a id="parameters"></a>

- `trackEvents`: Whether or not events are tracked.

Here's an example:

```json
{
  "environmentKey": "environment-key-123abc",
  "instructions": [ { "kind": "updateTrackEvents", "trackEvents": true } ]
}
```

#### updateTrackEventsFallthrough<a id="updatetrackeventsfallthrough"></a>

Updates whether or not LaunchDarkly tracks events for the feature flag, for the default rule.

##### Parameters<a id="parameters"></a>

- `trackEvents`: Whether or not events are tracked.

Here's an example:

```json
{
  "environmentKey": "environment-key-123abc",
  "instructions": [ { "kind": "updateTrackEventsFallthrough", "trackEvents": true } ]
}
```

#### updateVariation<a id="updatevariation"></a>

Updates a variation of the flag.

##### Parameters<a id="parameters"></a>

- `variationId`: The ID of the variation to update.
- `name`: (Optional) The updated variation name.
- `value`: (Optional) The updated variation value.
- `description`: (Optional) The updated variation description.

Here's an example:

```json
{
	"instructions": [ { "kind": "updateVariation", "variationId": "2f43f67c-3e4e-4945-a18a-26559378ca00", "value": 20 } ]
}
```

</details><br />

<details>
<summary>Click to expand instructions for <strong>updating flag settings</strong></summary>

These instructions do not require the `environmentKey` parameter. They make changes that apply to the flag across all environments.

#### addCustomProperties<a id="addcustomproperties"></a>

Adds a new custom property to the feature flag. Custom properties are used to associate feature flags with LaunchDarkly integrations. For example, if you create an integration with an issue tracking service, you may want to associate a flag with a list of issues related to a feature's development.

##### Parameters<a id="parameters"></a>

 - `key`: The custom property key.
 - `name`: The custom property name.
 - `values`: A list of the associated values for the custom property.

Here's an example:

```json
{
	"instructions": [{
		"kind": "addCustomProperties",
		"key": "example-custom-property",
		"name": "Example custom property",
		"values": ["value1", "value2"]
	}]
}
```

#### addTags<a id="addtags"></a>

Adds tags to the feature flag.

##### Parameters<a id="parameters"></a>

- `values`: A list of tags to add.

Here's an example:

```json
{
  "instructions": [ { "kind": "addTags", "values": ["tag1", "tag2"] } ]
}
```

#### makeFlagPermanent<a id="makeflagpermanent"></a>

Marks the feature flag as permanent. LaunchDarkly does not prompt you to remove permanent flags, even if one variation is rolled out to all your customers.

Here's an example:

```json
{
  "instructions": [ { "kind": "makeFlagPermanent" } ]
}
```

#### makeFlagTemporary<a id="makeflagtemporary"></a>

Marks the feature flag as temporary.

Here's an example:

```json
{
  "instructions": [ { "kind": "makeFlagTemporary" } ]
}
```

#### removeCustomProperties<a id="removecustomproperties"></a>

Removes the associated values from a custom property. If all the associated values are removed, this instruction also removes the custom property.

##### Parameters<a id="parameters"></a>

 - `key`: The custom property key.
 - `values`: A list of the associated values to remove from the custom property.

```json
{
	"instructions": [{
		"kind": "replaceCustomProperties",
		"key": "example-custom-property",
		"values": ["value1", "value2"]
	}]
}
```

#### removeMaintainer<a id="removemaintainer"></a>

Removes the flag's maintainer. To set a new maintainer, use the flag's **Settings** tab in the LaunchDarkly user interface.

Here's an example:

```json
{
  "instructions": [ { "kind": "removeMaintainer" } ]
}
```

#### removeTags<a id="removetags"></a>

Removes tags from the feature flag.

##### Parameters<a id="parameters"></a>

- `values`: A list of tags to remove.

Here's an example:

```json
{
  "instructions": [ { "kind": "removeTags", "values": ["tag1", "tag2"] } ]
}
```

#### replaceCustomProperties<a id="replacecustomproperties"></a>

Replaces the existing associated values for a custom property with the new values.

##### Parameters<a id="parameters"></a>

 - `key`: The custom property key.
 - `name`: The custom property name.
 - `values`: A list of the new associated values for the custom property.

Here's an example:

```json
{
 "instructions": [{
   "kind": "replaceCustomProperties",
   "key": "example-custom-property",
   "name": "Example custom property",
   "values": ["value1", "value2"]
 }]
}
```

#### turnOffClientSideAvailability<a id="turnoffclientsideavailability"></a>

Turns off client-side SDK availability for the flag. This is equivalent to unchecking the **SDKs using Mobile Key** and/or **SDKs using client-side ID** boxes for the flag. If you're using a client-side or mobile SDK, you must expose your feature flags in order for the client-side or mobile SDKs to evaluate them.

##### Parameters<a id="parameters"></a>

- `value`: Use "usingMobileKey" to turn off availability for mobile SDKs. Use "usingEnvironmentId" to turn on availability for client-side SDKs.

Here's an example:

```json
{
  "instructions": [ { "kind": "turnOffClientSideAvailability", "value": "usingMobileKey" } ]
}
```

#### turnOnClientSideAvailability<a id="turnonclientsideavailability"></a>

Turns on client-side SDK availability for the flag. This is equivalent to unchecking the **SDKs using Mobile Key** and/or **SDKs using client-side ID** boxes for the flag. If you're using a client-side or mobile SDK, you must expose your feature flags in order for the client-side or mobile SDKs to evaluate them.

##### Parameters<a id="parameters"></a>

- `value`: Use "usingMobileKey" to turn on availability for mobile SDKs. Use "usingEnvironmentId" to turn on availability for client-side SDKs.

Here's an example:

```json
{
  "instructions": [ { "kind": "turnOnClientSideAvailability", "value": "usingMobileKey" } ]
}
```

#### updateDescription<a id="updatedescription"></a>

Updates the feature flag description.

##### Parameters<a id="parameters"></a>

- `value`: The new description.

Here's an example:

```json
{
  "instructions": [ { "kind": "updateDescription", "value": "Updated flag description" } ]
}
```
#### updateMaintainerMember<a id="updatemaintainermember"></a>

Updates the maintainer of the flag to an existing member and removes the existing maintainer.

##### Parameters<a id="parameters"></a>

- `value`: The ID of the member.

Here's an example:

```json
{
  "instructions": [ { "kind": "updateMaintainerMember", "value": "61e9b714fd47591727db558a" } ]
}
```

#### updateMaintainerTeam<a id="updatemaintainerteam"></a>

Updates the maintainer of the flag to an existing team and removes the existing maintainer.

##### Parameters<a id="parameters"></a>

- `value`: The key of the team.

Here's an example:

```json
{
  "instructions": [ { "kind": "updateMaintainerTeam", "value": "example-team-key" } ]
}
```

#### updateName<a id="updatename"></a>

Updates the feature flag name.

##### Parameters<a id="parameters"></a>

- `value`: The new name.

Here's an example:

```json
{
  "instructions": [ { "kind": "updateName", "value": "Updated flag name" } ]
}
```

</details><br />

<details>
<summary>Click to expand instructions for <strong>updating the flag lifecycle</strong></summary>

These instructions do not require the `environmentKey` parameter. They make changes that apply to the flag across all environments.

#### archiveFlag<a id="archiveflag"></a>

Archives the feature flag. This retires it from LaunchDarkly without deleting it. You cannot archive a flag that is a prerequisite of other flags.

```json
{
  "instructions": [ { "kind": "archiveFlag" } ]
}
```

#### deleteFlag<a id="deleteflag"></a>

Deletes the feature flag and its rules. You cannot restore a deleted flag. If this flag is requested again, the flag value defined in code will be returned for all contexts.

Here's an example:

```json
{
  "instructions": [ { "kind": "deleteFlag" } ]
}
```

#### deprecateFlag<a id="deprecateflag"></a>

Deprecates the feature flag. This hides it from the live flags list without archiving or deleting it.

Here's an example:

```json
{
  "instructions": [ { "kind": "deprecateFlag" } ]
}
```

#### restoreDeprecatedFlag<a id="restoredeprecatedflag"></a>

Restores the feature flag if it was previously deprecated.

Here's an example:

```json
{
  "instructions": [ { "kind": "restoreDeprecatedFlag" } ]
}
```

#### restoreFlag<a id="restoreflag"></a>

Restores the feature flag if it was previously archived.

Here's an example:

```json
{
  "instructions": [ { "kind": "restoreFlag" } ]
}
```

</details>

### Using JSON patches on a feature flag<a id="using-json-patches-on-a-feature-flag"></a>

If you do not include the semantic patch header described above, you can use a [JSON patch](https://apidocs.launchdarkly.com) or [JSON merge patch](https://datatracker.ietf.org/doc/html/rfc7386) representation of the desired changes.

In the JSON patch representation, use a JSON pointer in the `path` element to describe what field to change. Use the [Get feature flag](https://apidocs.launchdarkly.com) endpoint to find the field you want to update.

There are a few special cases to keep in mind when determining the value of the `path` element:

  * To add an individual target to a specific variation if the flag variation already has individual targets, the path for the JSON patch operation is:

  ```json
  [
    {
      "op": "add",
      "path": "/environments/devint/targets/0/values/-",
      "value": "TestClient10"
    }
  ]
  ```

  * To add an individual target to a specific variation if the flag variation does not already have individual targets, the path for the JSON patch operation is:

  ```json
  [
    {
      "op": "add",
      "path": "/environments/devint/targets/-",
      "value": { "variation": 0, "values": ["TestClient10"] }
    }
  ]
  ```

  * To add a flag to a release pipeline, the path for the JSON patch operation is:

  ```json
  [
    {
      "op": "add",
      "path": "/releasePipelineKey",
      "value": "example-release-pipeline-key"
    }
  ]
  ```

### Required approvals<a id="required-approvals"></a>
If a request attempts to alter a flag configuration in an environment where approvals are required for the flag, the request will fail with a 405. Changes to the flag configuration in that environment will require creating an [approval request](https://apidocs.launchdarkly.com) or a [workflow](https://apidocs.launchdarkly.com).

### Conflicts<a id="conflicts"></a>
If a flag configuration change made through this endpoint would cause a pending scheduled change or approval request to fail, this endpoint will return a 400. You can ignore this check by adding an `ignoreConflicts` query parameter set to `true`.

### Migration flags<a id="migration-flags"></a>
For migration flags, the cohort information is included in the `rules` property of a flag's response. You can update cohorts by updating `rules`. Default cohort information is included in the `fallthrough` property of a flag's response. You can update the default cohort by updating `fallthrough`.
When you update the rollout for a cohort or the default cohort through the API, provide a rollout instead of a single `variationId`.
To learn more, read [Migration Flags](https://docs.launchdarkly.com/home/flag-types/migration-flags).


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
update_feature_flag_response = launchdarkly.feature_flags.update_feature_flag(
    patch=[
        {
            "op": "replace",
            "path": "/exampleField",
            "value": None,
        }
    ],
    project_key="projectKey_example",
    feature_flag_key="featureFlagKey_example",
    comment="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### patch: [`JSONPatch`](./launch_darkly_python_sdk/type/json_patch.py)<a id="patch-jsonpatchlaunch_darkly_python_sdktypejson_patchpy"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### feature_flag_key: `str`<a id="feature_flag_key-str"></a>

The feature flag key. The key identifies the flag in your code.

##### comment: `str`<a id="comment-str"></a>

Optional comment

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`PatchWithComment`](./launch_darkly_python_sdk/type/patch_with_comment.py)
#### 🔄 Return<a id="🔄-return"></a>

[`FeatureFlag`](./launch_darkly_python_sdk/pydantic/feature_flag.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/flags/{projectKey}/{featureFlagKey}` `patch`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.feature_flags_(beta).get_migration_safety_issues`<a id="launchdarklyfeature_flags_betaget_migration_safety_issues"></a>

Returns the migration safety issues that are associated with the POSTed flag patch. The patch must use the semantic patch format for updating feature flags.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_migration_safety_issues_response = launchdarkly.feature_flags_(beta).get_migration_safety_issues(
    instructions=[
        {
            "key": None,
        }
    ],
    project_key="projectKey_example",
    flag_key="flagKey_example",
    environment_key="environmentKey_example",
    comment="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### instructions: [`Instructions`](./launch_darkly_python_sdk/type/instructions.py)<a id="instructions-instructionslaunch_darkly_python_sdktypeinstructionspy"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### flag_key: `str`<a id="flag_key-str"></a>

The migration flag key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

##### comment: `str`<a id="comment-str"></a>

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`FlagSempatch`](./launch_darkly_python_sdk/type/flag_sempatch.py)
#### 🔄 Return<a id="🔄-return"></a>

[`FeatureFlagsBetaGetMigrationSafetyIssuesResponse`](./launch_darkly_python_sdk/pydantic/feature_flags_beta_get_migration_safety_issues_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/projects/{projectKey}/flags/{flagKey}/environments/{environmentKey}/migration-safety-issues` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.feature_flags_(beta).list_dependent_flags`<a id="launchdarklyfeature_flags_betalist_dependent_flags"></a>

> ### Flag prerequisites is an Enterprise feature
>
> Flag prerequisites is available to customers on an Enterprise plan. To learn more, [read about our pricing](https://launchdarkly.com/pricing/). To upgrade your plan, [contact Sales](https://launchdarkly.com/contact-sales/).

List dependent flags across all environments for the flag specified in the path parameters. A dependent flag is a flag that uses another flag as a prerequisite. To learn more, read [Flag prerequisites](https://docs.launchdarkly.com/home/targeting-flags/prerequisites).


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_dependent_flags_response = launchdarkly.feature_flags_(beta).list_dependent_flags(
    project_key="projectKey_example",
    feature_flag_key="featureFlagKey_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### feature_flag_key: `str`<a id="feature_flag_key-str"></a>

The feature flag key

#### 🔄 Return<a id="🔄-return"></a>

[`MultiEnvironmentDependentFlags`](./launch_darkly_python_sdk/pydantic/multi_environment_dependent_flags.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/flags/{projectKey}/{featureFlagKey}/dependent-flags` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.feature_flags_(beta).list_dependent_flags_by_env`<a id="launchdarklyfeature_flags_betalist_dependent_flags_by_env"></a>

> ### Flag prerequisites is an Enterprise feature
>
> Flag prerequisites is available to customers on an Enterprise plan. To learn more, [read about our pricing](https://launchdarkly.com/pricing/). To upgrade your plan, [contact Sales](https://launchdarkly.com/contact-sales/).

List dependent flags across all environments for the flag specified in the path parameters. A dependent flag is a flag that uses another flag as a prerequisite. To learn more, read [Flag prerequisites](https://docs.launchdarkly.com/home/targeting-flags/prerequisites).


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_dependent_flags_by_env_response = launchdarkly.feature_flags_(beta).list_dependent_flags_by_env(
    project_key="projectKey_example",
    environment_key="environmentKey_example",
    feature_flag_key="featureFlagKey_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

##### feature_flag_key: `str`<a id="feature_flag_key-str"></a>

The feature flag key

#### 🔄 Return<a id="🔄-return"></a>

[`DependentFlagsByEnvironment`](./launch_darkly_python_sdk/pydantic/dependent_flags_by_environment.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/flags/{projectKey}/{environmentKey}/{featureFlagKey}/dependent-flags` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.flag_links_(beta).create_flag_link`<a id="launchdarklyflag_links_betacreate_flag_link"></a>

Create a new flag link. Flag links let you reference external resources and associate them with your flags.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
create_flag_link_response = launchdarkly.flag_links_(beta).create_flag_link(
    project_key="projectKey_example",
    feature_flag_key="featureFlagKey_example",
    title="Example link title",
    description="Example link description",
    key="flag-link-key-123abc",
    integration_key="string_example",
    timestamp=1,
    deep_link="https://example.com/archives/123123123",
    metadata={
        "key": "string_example",
    },
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### feature_flag_key: `str`<a id="feature_flag_key-str"></a>

The feature flag key

##### title: `str`<a id="title-str"></a>

The title of the flag link

##### description: `str`<a id="description-str"></a>

The description of the flag link

##### key: `str`<a id="key-str"></a>

The flag link key

##### integration_key: `str`<a id="integration_key-str"></a>

The integration key for an integration whose <code>manifest.json</code> includes the <code>flagLink</code> capability, if this is a flag link for an existing integration. Do not include for URL flag links.

##### timestamp: `int`<a id="timestamp-int"></a>

##### deep_link: `str`<a id="deep_link-str"></a>

The URL for the external resource you are linking the flag to

##### metadata: [`FlagLinkPostMetadata`](./launch_darkly_python_sdk/type/flag_link_post_metadata.py)<a id="metadata-flaglinkpostmetadatalaunch_darkly_python_sdktypeflag_link_post_metadatapy"></a>

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`FlagLinkPost`](./launch_darkly_python_sdk/type/flag_link_post.py)
#### 🔄 Return<a id="🔄-return"></a>

[`FlagLinkRep`](./launch_darkly_python_sdk/pydantic/flag_link_rep.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/flag-links/projects/{projectKey}/flags/{featureFlagKey}` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.flag_links_(beta).delete_flag_link`<a id="launchdarklyflag_links_betadelete_flag_link"></a>

Delete a flag link by ID or key.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
launchdarkly.flag_links_(beta).delete_flag_link(
    project_key="projectKey_example",
    feature_flag_key="featureFlagKey_example",
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### feature_flag_key: `str`<a id="feature_flag_key-str"></a>

The feature flag key

##### id: `str`<a id="id-str"></a>

The flag link ID or Key

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/flag-links/projects/{projectKey}/flags/{featureFlagKey}/{id}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.flag_links_(beta).list_links`<a id="launchdarklyflag_links_betalist_links"></a>

Get a list of all flag links.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_links_response = launchdarkly.flag_links_(beta).list_links(
    project_key="projectKey_example",
    feature_flag_key="featureFlagKey_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### feature_flag_key: `str`<a id="feature_flag_key-str"></a>

The feature flag key

#### 🔄 Return<a id="🔄-return"></a>

[`FlagLinkCollectionRep`](./launch_darkly_python_sdk/pydantic/flag_link_collection_rep.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/flag-links/projects/{projectKey}/flags/{featureFlagKey}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.flag_links_(beta).update_flag_link`<a id="launchdarklyflag_links_betaupdate_flag_link"></a>

Update a flag link. Updating a flag link uses a [JSON patch](https://datatracker.ietf.org/doc/html/rfc6902) representation of the desired changes. To learn more, read [Updates](https://apidocs.launchdarkly.com).

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
update_flag_link_response = launchdarkly.flag_links_(beta).update_flag_link(
    body=[{"op":"replace","path":"/title","value":"Updated flag link title"}],
    project_key="projectKey_example",
    feature_flag_key="featureFlagKey_example",
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### feature_flag_key: `str`<a id="feature_flag_key-str"></a>

The feature flag key

##### id: `str`<a id="id-str"></a>

The flag link ID

##### requestBody: [`JSONPatch`](./launch_darkly_python_sdk/type/json_patch.py)<a id="requestbody-jsonpatchlaunch_darkly_python_sdktypejson_patchpy"></a>

#### 🔄 Return<a id="🔄-return"></a>

[`FlagLinkRep`](./launch_darkly_python_sdk/pydantic/flag_link_rep.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/flag-links/projects/{projectKey}/flags/{featureFlagKey}/{id}` `patch`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.flag_triggers.create_trigger_workflow`<a id="launchdarklyflag_triggerscreate_trigger_workflow"></a>

Create a new flag trigger.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
create_trigger_workflow_response = launchdarkly.flag_triggers.create_trigger_workflow(
    integration_key="generic-trigger",
    project_key="projectKey_example",
    environment_key="environmentKey_example",
    feature_flag_key="featureFlagKey_example",
    comment="example comment",
    instructions=[{
    "key": None,
}],
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### integration_key: `str`<a id="integration_key-str"></a>

The unique identifier of the integration for your trigger. Use <code>generic-trigger</code> for integrations not explicitly supported.

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

##### feature_flag_key: `str`<a id="feature_flag_key-str"></a>

The feature flag key

##### comment: `str`<a id="comment-str"></a>

Optional comment describing the trigger

##### instructions: List[[`Instruction`](./launch_darkly_python_sdk/type/instruction.py)]<a id="instructions-listinstructionlaunch_darkly_python_sdktypeinstructionpy"></a>

The action to perform when triggering. This should be an array with a single object that looks like <code>{\\\"kind\\\": \\\"flag_action\\\"}</code>. Supported flag actions are <code>turnFlagOn</code> and <code>turnFlagOff</code>.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`TriggerPost`](./launch_darkly_python_sdk/type/trigger_post.py)
#### 🔄 Return<a id="🔄-return"></a>

[`TriggerWorkflowRep`](./launch_darkly_python_sdk/pydantic/trigger_workflow_rep.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/flags/{projectKey}/{featureFlagKey}/triggers/{environmentKey}` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.flag_triggers.delete_by_id`<a id="launchdarklyflag_triggersdelete_by_id"></a>

Delete a flag trigger by ID.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
launchdarkly.flag_triggers.delete_by_id(
    project_key="projectKey_example",
    environment_key="environmentKey_example",
    feature_flag_key="featureFlagKey_example",
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

##### feature_flag_key: `str`<a id="feature_flag_key-str"></a>

The feature flag key

##### id: `str`<a id="id-str"></a>

The flag trigger ID

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/flags/{projectKey}/{featureFlagKey}/triggers/{environmentKey}/{id}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.flag_triggers.get_trigger_by_id`<a id="launchdarklyflag_triggersget_trigger_by_id"></a>

Get a flag trigger by ID.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_trigger_by_id_response = launchdarkly.flag_triggers.get_trigger_by_id(
    project_key="projectKey_example",
    feature_flag_key="featureFlagKey_example",
    environment_key="environmentKey_example",
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### feature_flag_key: `str`<a id="feature_flag_key-str"></a>

The feature flag key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

##### id: `str`<a id="id-str"></a>

The flag trigger ID

#### 🔄 Return<a id="🔄-return"></a>

[`TriggerWorkflowRep`](./launch_darkly_python_sdk/pydantic/trigger_workflow_rep.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/flags/{projectKey}/{featureFlagKey}/triggers/{environmentKey}/{id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.flag_triggers.list_trigger_workflows`<a id="launchdarklyflag_triggerslist_trigger_workflows"></a>

Get a list of all flag triggers.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_trigger_workflows_response = launchdarkly.flag_triggers.list_trigger_workflows(
    project_key="projectKey_example",
    environment_key="environmentKey_example",
    feature_flag_key="featureFlagKey_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

##### feature_flag_key: `str`<a id="feature_flag_key-str"></a>

The feature flag key

#### 🔄 Return<a id="🔄-return"></a>

[`TriggerWorkflowCollectionRep`](./launch_darkly_python_sdk/pydantic/trigger_workflow_collection_rep.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/flags/{projectKey}/{featureFlagKey}/triggers/{environmentKey}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.flag_triggers.update_trigger_workflow_patch`<a id="launchdarklyflag_triggersupdate_trigger_workflow_patch"></a>

Update a flag trigger. Updating a flag trigger uses the semantic patch format.

To make a semantic patch request, you must append `domain-model=launchdarkly.semanticpatch` to your `Content-Type` header. To learn more, read [Updates using semantic patch](https://apidocs.launchdarkly.com).

### Instructions<a id="instructions"></a>

Semantic patch requests support the following `kind` instructions for updating flag triggers.

<details>
<summary>Click to expand instructions for <strong>updating flag triggers</strong></summary>

#### replaceTriggerActionInstructions<a id="replacetriggeractioninstructions"></a>

Removes the existing trigger action and replaces it with the new instructions.

##### Parameters<a id="parameters"></a>

- `value`: An array of the new `kind`s of actions to perform when triggering. Supported flag actions are `turnFlagOn` and `turnFlagOff`.

Here's an example that replaces the existing action with new instructions to turn flag targeting off:

```json
{
  "instructions": [
    {
      "kind": "replaceTriggerActionInstructions",
      "value": [ {"kind": "turnFlagOff"} ]
    }
  ]
}
```

#### cycleTriggerUrl<a id="cycletriggerurl"></a>

Generates a new URL for this trigger. You must update any clients using the trigger to use this new URL.

Here's an example:

```json
{
  "instructions": [{ "kind": "cycleTriggerUrl" }]
}
```

#### disableTrigger<a id="disabletrigger"></a>

Disables the trigger. This saves the trigger configuration, but the trigger stops running. To re-enable, use `enableTrigger`.

Here's an example:

```json
{
  "instructions": [{ "kind": "disableTrigger" }]
}
```

#### enableTrigger<a id="enabletrigger"></a>

Enables the trigger. If you previously disabled the trigger, it begins running again.

Here's an example:

```json
{
  "instructions": [{ "kind": "enableTrigger" }]
}
```

</details>


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
update_trigger_workflow_patch_response = launchdarkly.flag_triggers.update_trigger_workflow_patch(
    project_key="projectKey_example",
    environment_key="environmentKey_example",
    feature_flag_key="featureFlagKey_example",
    id="id_example",
    comment="optional comment",
    instructions=[{
    "key": None,
}],
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

##### feature_flag_key: `str`<a id="feature_flag_key-str"></a>

The feature flag key

##### id: `str`<a id="id-str"></a>

The flag trigger ID

##### comment: `str`<a id="comment-str"></a>

Optional comment describing the update

##### instructions: List[[`Instruction`](./launch_darkly_python_sdk/type/instruction.py)]<a id="instructions-listinstructionlaunch_darkly_python_sdktypeinstructionpy"></a>

The instructions to perform when updating. This should be an array with objects that look like <code>{\\\"kind\\\": \\\"trigger_action\\\"}</code>.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`FlagTriggerInput`](./launch_darkly_python_sdk/type/flag_trigger_input.py)
#### 🔄 Return<a id="🔄-return"></a>

[`TriggerWorkflowRep`](./launch_darkly_python_sdk/pydantic/trigger_workflow_rep.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/flags/{projectKey}/{featureFlagKey}/triggers/{environmentKey}/{id}` `patch`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.follow_flags.flag_followers_list`<a id="launchdarklyfollow_flagsflag_followers_list"></a>

Get a list of members following a flag in a project and environment

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
flag_followers_list_response = launchdarkly.follow_flags.flag_followers_list(
    project_key="projectKey_example",
    feature_flag_key="featureFlagKey_example",
    environment_key="environmentKey_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### feature_flag_key: `str`<a id="feature_flag_key-str"></a>

The feature flag key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

#### 🔄 Return<a id="🔄-return"></a>

[`FlagFollowersGetRep`](./launch_darkly_python_sdk/pydantic/flag_followers_get_rep.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/projects/{projectKey}/flags/{featureFlagKey}/environments/{environmentKey}/followers` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.follow_flags.get_all_flag_followers`<a id="launchdarklyfollow_flagsget_all_flag_followers"></a>

Get followers of all flags in a given environment and project

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_all_flag_followers_response = launchdarkly.follow_flags.get_all_flag_followers(
    project_key="projectKey_example",
    environment_key="environmentKey_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

#### 🔄 Return<a id="🔄-return"></a>

[`FlagFollowersByProjEnvGetRep`](./launch_darkly_python_sdk/pydantic/flag_followers_by_proj_env_get_rep.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/projects/{projectKey}/environments/{environmentKey}/followers` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.follow_flags.member_follower`<a id="launchdarklyfollow_flagsmember_follower"></a>

Add a member as a follower to a flag in a project and environment

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
launchdarkly.follow_flags.member_follower(
    project_key="projectKey_example",
    feature_flag_key="featureFlagKey_example",
    environment_key="environmentKey_example",
    member_id="memberId_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### feature_flag_key: `str`<a id="feature_flag_key-str"></a>

The feature flag key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

##### member_id: `str`<a id="member_id-str"></a>

The memberId of the member to add as a follower of the flag. Reader roles can only add themselves.

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/projects/{projectKey}/flags/{featureFlagKey}/environments/{environmentKey}/followers/{memberId}` `put`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.follow_flags.remove_follower`<a id="launchdarklyfollow_flagsremove_follower"></a>

Remove a member as a follower to a flag in a project and environment

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
launchdarkly.follow_flags.remove_follower(
    project_key="projectKey_example",
    feature_flag_key="featureFlagKey_example",
    environment_key="environmentKey_example",
    member_id="memberId_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### feature_flag_key: `str`<a id="feature_flag_key-str"></a>

The feature flag key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

##### member_id: `str`<a id="member_id-str"></a>

The memberId of the member to remove as a follower of the flag. Reader roles can only remove themselves.

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/projects/{projectKey}/flags/{featureFlagKey}/environments/{environmentKey}/followers/{memberId}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.insights_charts_(beta).deployment_frequency_chart_data`<a id="launchdarklyinsights_charts_betadeployment_frequency_chart_data"></a>

Get deployment frequency chart data. Engineering insights displays deployment frequency data in the [deployment frequency metric view](https://docs.launchdarkly.com/home/engineering-insights/metrics/deployment).

### Expanding the chart response<a id="expanding-the-chart-response"></a>

LaunchDarkly supports expanding the chart response to include additional fields.

To expand the response, append the `expand` query parameter and include the following:

* `metrics` includes details on the metrics related to deployment frequency

For example, use `?expand=metrics` to include the `metrics` field in the response. By default, this field is **not** included in the response.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
deployment_frequency_chart_data_response = launchdarkly.insights_charts_(beta).deployment_frequency_chart_data(
    project_key="string_example",
    environment_key="string_example",
    application_key="string_example",
    _from="1970-01-01T00:00:00.00Z",
    to="1970-01-01T00:00:00.00Z",
    bucket_type="string_example",
    bucket_ms=1,
    group_by="string_example",
    expand="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

##### application_key: `str`<a id="application_key-str"></a>

Comma separated list of application keys

##### _from: `datetime`<a id="_from-datetime"></a>

Unix timestamp in milliseconds. Default value is 7 days ago.

##### to: `datetime`<a id="to-datetime"></a>

Unix timestamp in milliseconds. Default value is now.

##### bucket_type: `str`<a id="bucket_type-str"></a>

Specify type of bucket. Options: `rolling`, `hour`, `day`. Default: `rolling`.

##### bucket_ms: `int`<a id="bucket_ms-int"></a>

Duration of intervals for x-axis in milliseconds. Default value is one day (`86400000` milliseconds).

##### group_by: `str`<a id="group_by-str"></a>

Options: `application`, `kind`

##### expand: `str`<a id="expand-str"></a>

Options: `metrics`

#### 🔄 Return<a id="🔄-return"></a>

[`InsightsChart`](./launch_darkly_python_sdk/pydantic/insights_chart.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/engineering-insights/charts/deployments/frequency` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.insights_charts_(beta).get_flag_status_chart_data`<a id="launchdarklyinsights_charts_betaget_flag_status_chart_data"></a>

Get flag status chart data. To learn more, read [Using the flag status chart](https://docs.launchdarkly.com/home/engineering-insights/metrics/flag-health#using-the-flag-status-chart).

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_flag_status_chart_data_response = launchdarkly.insights_charts_(beta).get_flag_status_chart_data(
    project_key="projectKey_example",
    environment_key="environmentKey_example",
    application_key="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

##### application_key: `str`<a id="application_key-str"></a>

Comma separated list of application keys

#### 🔄 Return<a id="🔄-return"></a>

[`InsightsChart`](./launch_darkly_python_sdk/pydantic/insights_chart.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/engineering-insights/charts/flags/status` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.insights_charts_(beta).lead_time_chart_data`<a id="launchdarklyinsights_charts_betalead_time_chart_data"></a>

Get lead time chart data. The engineering insights UI displays lead time data in the [lead time metric view](https://docs.launchdarkly.com/home/engineering-insights/metrics/lead-time).

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
lead_time_chart_data_response = launchdarkly.insights_charts_(beta).lead_time_chart_data(
    project_key="projectKey_example",
    environment_key="string_example",
    application_key="string_example",
    _from=1,
    to=1,
    bucket_type="string_example",
    bucket_ms=1,
    group_by="string_example",
    expand="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

##### application_key: `str`<a id="application_key-str"></a>

Comma separated list of application keys

##### _from: `int`<a id="_from-int"></a>

Unix timestamp in milliseconds. Default value is 7 days ago.

##### to: `int`<a id="to-int"></a>

Unix timestamp in milliseconds. Default value is now.

##### bucket_type: `str`<a id="bucket_type-str"></a>

Specify type of bucket. Options: `rolling`, `hour`, `day`. Default: `rolling`.

##### bucket_ms: `int`<a id="bucket_ms-int"></a>

Duration of intervals for x-axis in milliseconds. Default value is one day (`86400000` milliseconds).

##### group_by: `str`<a id="group_by-str"></a>

Options: `application`, `stage`. Default: `stage`.

##### expand: `str`<a id="expand-str"></a>

Options: `metrics`, `percentiles`.

#### 🔄 Return<a id="🔄-return"></a>

[`InsightsChart`](./launch_darkly_python_sdk/pydantic/insights_chart.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/engineering-insights/charts/lead-time` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.insights_charts_(beta).release_frequency_data`<a id="launchdarklyinsights_charts_betarelease_frequency_data"></a>

Get release frequency chart data. Engineering insights displays release frequency data in the [release frequency metric view](https://docs.launchdarkly.com/home/engineering-insights/metrics/release).

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
release_frequency_data_response = launchdarkly.insights_charts_(beta).release_frequency_data(
    project_key="projectKey_example",
    environment_key="environmentKey_example",
    application_key="string_example",
    has_experiments=True,
    _global="string_example",
    group_by="string_example",
    _from="1970-01-01T00:00:00.00Z",
    to="1970-01-01T00:00:00.00Z",
    bucket_type="string_example",
    bucket_ms=1,
    expand="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

##### application_key: `str`<a id="application_key-str"></a>

Comma separated list of application keys

##### has_experiments: `bool`<a id="has_experiments-bool"></a>

Filter events to those associated with an experiment (`true`) or without an experiment (`false`)

##### _global: `str`<a id="_global-str"></a>

Filter to include or exclude global events. Default value is `include`. Options: `include`, `exclude`

##### group_by: `str`<a id="group_by-str"></a>

Property to group results by. Options: `impact`

##### _from: `datetime`<a id="_from-datetime"></a>

Unix timestamp in milliseconds. Default value is 7 days ago.

##### to: `datetime`<a id="to-datetime"></a>

Unix timestamp in milliseconds. Default value is now.

##### bucket_type: `str`<a id="bucket_type-str"></a>

Specify type of bucket. Options: `rolling`, `hour`, `day`. Default: `rolling`.

##### bucket_ms: `int`<a id="bucket_ms-int"></a>

Duration of intervals for x-axis in milliseconds. Default value is one day (`86400000` milliseconds).

##### expand: `str`<a id="expand-str"></a>

Options: `metrics`

#### 🔄 Return<a id="🔄-return"></a>

[`InsightsChart`](./launch_darkly_python_sdk/pydantic/insights_chart.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/engineering-insights/charts/releases/frequency` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.insights_charts_(beta).stale_flags_chart_data`<a id="launchdarklyinsights_charts_betastale_flags_chart_data"></a>

Get stale flags chart data. Engineering insights displays stale flags data in the [flag health metric view](https://docs.launchdarkly.com/home/engineering-insights/metrics/flag-health).

### Expanding the chart response<a id="expanding-the-chart-response"></a>

LaunchDarkly supports expanding the chart response to include additional fields.

To expand the response, append the `expand` query parameter and include the following:

* `metrics` includes details on the metrics related to stale flags

For example, use `?expand=metrics` to include the `metrics` field in the response. By default, this field is **not** included in the response.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
stale_flags_chart_data_response = launchdarkly.insights_charts_(beta).stale_flags_chart_data(
    project_key="projectKey_example",
    environment_key="environmentKey_example",
    application_key="string_example",
    group_by="string_example",
    maintainer_id="string_example",
    maintainer_team_key="string_example",
    expand="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

##### application_key: `str`<a id="application_key-str"></a>

Comma separated list of application keys

##### group_by: `str`<a id="group_by-str"></a>

Property to group results by. Options: `maintainer`

##### maintainer_id: `str`<a id="maintainer_id-str"></a>

Comma-separated list of individual maintainers to filter results.

##### maintainer_team_key: `str`<a id="maintainer_team_key-str"></a>

Comma-separated list of team maintainer keys to filter results.

##### expand: `str`<a id="expand-str"></a>

Options: `metrics`

#### 🔄 Return<a id="🔄-return"></a>

[`InsightsChart`](./launch_darkly_python_sdk/pydantic/insights_chart.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/engineering-insights/charts/flags/stale` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.insights_deployments_(beta).create_deployment_event`<a id="launchdarklyinsights_deployments_betacreate_deployment_event"></a>

Create deployment event

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
launchdarkly.insights_deployments_(beta).create_deployment_event(
    version="a90a8a2",
    project_key="default",
    environment_key="production",
    application_key="billing-service",
    event_type="started",
    application_name="Billing Service",
    application_kind="server",
    version_name="v1.0.0",
    event_time=1,
    event_metadata={
        "key": None,
    },
    deployment_metadata={
        "key": None,
    },
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### version: `str`<a id="version-str"></a>

The application version. You can set the application version to any string that includes only letters, numbers, periods (<code>.</code>), hyphens (<code>-</code>), or underscores (<code>_</code>).<br/><br/>We recommend setting the application version to at least the first seven characters of the SHA or to the tag of the GitHub commit for this deployment.

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

##### application_key: `str`<a id="application_key-str"></a>

The application key. This defines the granularity at which you want to view your insights metrics. Typically it is the name of one of the GitHub repositories that you use in this project.<br/><br/>LaunchDarkly automatically creates a new application each time you send a unique application key.

##### event_type: `str`<a id="event_type-str"></a>

The event type

##### application_name: `str`<a id="application_name-str"></a>

The application name. This defines how the application is displayed

##### application_kind: `str`<a id="application_kind-str"></a>

The kind of application. Default: <code>server</code>

##### version_name: `str`<a id="version_name-str"></a>

The version name. This defines how the version is displayed

##### event_time: `int`<a id="event_time-int"></a>

##### event_metadata: [`PostDeploymentEventInputEventMetadata`](./launch_darkly_python_sdk/type/post_deployment_event_input_event_metadata.py)<a id="event_metadata-postdeploymenteventinputeventmetadatalaunch_darkly_python_sdktypepost_deployment_event_input_event_metadatapy"></a>

##### deployment_metadata: [`PostDeploymentEventInputDeploymentMetadata`](./launch_darkly_python_sdk/type/post_deployment_event_input_deployment_metadata.py)<a id="deployment_metadata-postdeploymenteventinputdeploymentmetadatalaunch_darkly_python_sdktypepost_deployment_event_input_deployment_metadatapy"></a>

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`PostDeploymentEventInput`](./launch_darkly_python_sdk/type/post_deployment_event_input.py)
#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/engineering-insights/deployment-events` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.insights_deployments_(beta).get_deployment_by_id`<a id="launchdarklyinsights_deployments_betaget_deployment_by_id"></a>

Get a deployment by ID.

The deployment ID is returned as part of the [List deployments](https://apidocs.launchdarkly.com) response. It is the `id` field of each element in the `items` array.

### Expanding the deployment response<a id="expanding-the-deployment-response"></a>

LaunchDarkly supports expanding the deployment response to include additional fields.

To expand the response, append the `expand` query parameter and include the following:

* `pullRequests` includes details on all of the pull requests associated with each deployment
* `flagReferences` includes details on all of the references to flags in each deployment

For example, use `?expand=pullRequests` to include the `pullRequests` field in the response. By default, this field is **not** included in the response.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_deployment_by_id_response = launchdarkly.insights_deployments_(beta).get_deployment_by_id(
    deployment_id="deploymentID_example",
    expand="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### deployment_id: `str`<a id="deployment_id-str"></a>

The deployment ID

##### expand: `str`<a id="expand-str"></a>

Expand properties in response. Options: `pullRequests`, `flagReferences`

#### 🔄 Return<a id="🔄-return"></a>

[`DeploymentRep`](./launch_darkly_python_sdk/pydantic/deployment_rep.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/engineering-insights/deployments/{deploymentID}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.insights_deployments_(beta).list_deployments`<a id="launchdarklyinsights_deployments_betalist_deployments"></a>

Get a list of deployments

### Expanding the deployment collection response<a id="expanding-the-deployment-collection-response"></a>

LaunchDarkly supports expanding the deployment collection response to include additional fields.

To expand the response, append the `expand` query parameter and include the following:

* `pullRequests` includes details on all of the pull requests associated with each deployment
* `flagReferences` includes details on all of the references to flags in each deployment

For example, use `?expand=pullRequests` to include the `pullRequests` field in the response. By default, this field is **not** included in the response.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_deployments_response = launchdarkly.insights_deployments_(beta).list_deployments(
    project_key="projectKey_example",
    environment_key="environmentKey_example",
    application_key="string_example",
    limit=1,
    expand="string_example",
    _from=1,
    to=1,
    after="string_example",
    before="string_example",
    kind="string_example",
    status="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

##### application_key: `str`<a id="application_key-str"></a>

Comma separated list of application keys

##### limit: `int`<a id="limit-int"></a>

The number of deployments to return. Default is 20. Maximum allowed is 100.

##### expand: `str`<a id="expand-str"></a>

Expand properties in response. Options: `pullRequests`, `flagReferences`

##### _from: `int`<a id="_from-int"></a>

Unix timestamp in milliseconds. Default value is 7 days ago.

##### to: `int`<a id="to-int"></a>

Unix timestamp in milliseconds. Default value is now.

##### after: `str`<a id="after-str"></a>

Identifier used for pagination

##### before: `str`<a id="before-str"></a>

Identifier used for pagination

##### kind: `str`<a id="kind-str"></a>

The deployment kind

##### status: `str`<a id="status-str"></a>

The deployment status

#### 🔄 Return<a id="🔄-return"></a>

[`DeploymentCollectionRep`](./launch_darkly_python_sdk/pydantic/deployment_collection_rep.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/engineering-insights/deployments` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.insights_deployments_(beta).update_deployment_by_id`<a id="launchdarklyinsights_deployments_betaupdate_deployment_by_id"></a>

Update a deployment by ID. Updating a deployment uses a [JSON patch](https://datatracker.ietf.org/doc/html/rfc6902) representation of the desired changes. To learn more, read [Updates](https://apidocs.launchdarkly.com).<br/><br/>The deployment ID is returned as part of the [List deployments](https://apidocs.launchdarkly.com) response. It is the `id` field of each element in the `items` array.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
update_deployment_by_id_response = launchdarkly.insights_deployments_(beta).update_deployment_by_id(
    body=[{"op":"replace","path":"/status","value":"finished"}],
    deployment_id="deploymentID_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### deployment_id: `str`<a id="deployment_id-str"></a>

The deployment ID

##### requestBody: [`JSONPatch`](./launch_darkly_python_sdk/type/json_patch.py)<a id="requestbody-jsonpatchlaunch_darkly_python_sdktypejson_patchpy"></a>

#### 🔄 Return<a id="🔄-return"></a>

[`DeploymentRep`](./launch_darkly_python_sdk/pydantic/deployment_rep.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/engineering-insights/deployments/{deploymentID}` `patch`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.insights_flag_events_(beta).list_flag_events`<a id="launchdarklyinsights_flag_events_betalist_flag_events"></a>

Get a list of flag events

### Expanding the flag event collection response<a id="expanding-the-flag-event-collection-response"></a>

LaunchDarkly supports expanding the flag event collection response to include additional fields.

To expand the response, append the `expand` query parameter and include the following:

* `experiments` includes details on all of the experiments run on each flag

For example, use `?expand=experiments` to include the `experiments` field in the response. By default, this field is **not** included in the response.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_flag_events_response = launchdarkly.insights_flag_events_(beta).list_flag_events(
    project_key="projectKey_example",
    environment_key="environmentKey_example",
    application_key="string_example",
    query="string_example",
    impact_size="string_example",
    has_experiments=True,
    _global="string_example",
    expand="string_example",
    limit=1,
    _from=1,
    to=1,
    after="string_example",
    before="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

##### application_key: `str`<a id="application_key-str"></a>

Comma separated list of application keys

##### query: `str`<a id="query-str"></a>

Filter events by flag key

##### impact_size: `str`<a id="impact_size-str"></a>

Filter events by impact size. A small impact created a less than 20% change in the proportion of end users receiving one or more flag variations. A medium impact created between a 20%-80% change. A large impact created a more than 80% change. Options: `none`, `small`, `medium`, `large`

##### has_experiments: `bool`<a id="has_experiments-bool"></a>

Filter events to those associated with an experiment (`true`) or without an experiment (`false`)

##### _global: `str`<a id="_global-str"></a>

Filter to include or exclude global events. Default value is `include`. Options: `include`, `exclude`

##### expand: `str`<a id="expand-str"></a>

Expand properties in response. Options: `experiments`

##### limit: `int`<a id="limit-int"></a>

The number of deployments to return. Default is 20. Maximum allowed is 100.

##### _from: `int`<a id="_from-int"></a>

Unix timestamp in milliseconds. Default value is 7 days ago.

##### to: `int`<a id="to-int"></a>

Unix timestamp in milliseconds. Default value is now.

##### after: `str`<a id="after-str"></a>

Identifier used for pagination

##### before: `str`<a id="before-str"></a>

Identifier used for pagination

#### 🔄 Return<a id="🔄-return"></a>

[`FlagEventCollectionRep`](./launch_darkly_python_sdk/pydantic/flag_event_collection_rep.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/engineering-insights/flag-events` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.insights_pull_requests_(beta).list_pull_requests`<a id="launchdarklyinsights_pull_requests_betalist_pull_requests"></a>

Get a list of pull requests

### Expanding the pull request collection response<a id="expanding-the-pull-request-collection-response"></a>

LaunchDarkly supports expanding the pull request collection response to include additional fields.

To expand the response, append the `expand` query parameter and include the following:

* `deployments` includes details on all of the deployments associated with each pull request
* `flagReferences` includes details on all of the references to flags in each pull request
* `leadTime` includes details about the lead time of the pull request for each stage

For example, use `?expand=deployments` to include the `deployments` field in the response. By default, this field is **not** included in the response.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_pull_requests_response = launchdarkly.insights_pull_requests_(beta).list_pull_requests(
    project_key="projectKey_example",
    environment_key="string_example",
    application_key="string_example",
    status="string_example",
    query="string_example",
    limit=1,
    expand="string_example",
    sort="string_example",
    _from="1970-01-01T00:00:00.00Z",
    to="1970-01-01T00:00:00.00Z",
    after="string_example",
    before="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### environment_key: `str`<a id="environment_key-str"></a>

Required if you are using the <code>sort</code> parameter's <code>leadTime</code> option to sort pull requests.

##### application_key: `str`<a id="application_key-str"></a>

Filter the results to pull requests deployed to a comma separated list of applications

##### status: `str`<a id="status-str"></a>

Filter results to pull requests with the given status. Options: `open`, `merged`, `closed`, `deployed`.

##### query: `str`<a id="query-str"></a>

Filter list of pull requests by title or author

##### limit: `int`<a id="limit-int"></a>

The number of pull requests to return. Default is 20. Maximum allowed is 100.

##### expand: `str`<a id="expand-str"></a>

Expand properties in response. Options: `deployments`, `flagReferences`, `leadTime`.

##### sort: `str`<a id="sort-str"></a>

Sort results. Requires the `environmentKey` to be set. Options: `leadTime` (asc) and `-leadTime` (desc). When query option is excluded, default sort is by created or merged date.

##### _from: `datetime`<a id="_from-datetime"></a>

Unix timestamp in milliseconds. Default value is 7 days ago.

##### to: `datetime`<a id="to-datetime"></a>

Unix timestamp in milliseconds. Default value is now.

##### after: `str`<a id="after-str"></a>

Identifier used for pagination

##### before: `str`<a id="before-str"></a>

Identifier used for pagination

#### 🔄 Return<a id="🔄-return"></a>

[`PullRequestCollectionRep`](./launch_darkly_python_sdk/pydantic/pull_request_collection_rep.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/engineering-insights/pull-requests` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.insights_repositories_(beta).associate_repositories_and_projects`<a id="launchdarklyinsights_repositories_betaassociate_repositories_and_projects"></a>

Associate repositories with projects

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
associate_repositories_and_projects_response = launchdarkly.insights_repositories_(beta).associate_repositories_and_projects(
    mappings=[
        {
            "repository_key": "launchdarkly/LaunchDarkly-Docs",
            "project_key": "default",
        }
    ],
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### mappings: List[`InsightsRepositoryProject`]<a id="mappings-listinsightsrepositoryproject"></a>

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`InsightsRepositoryProjectMappings`](./launch_darkly_python_sdk/type/insights_repository_project_mappings.py)
#### 🔄 Return<a id="🔄-return"></a>

[`InsightsRepositoryProjectCollection`](./launch_darkly_python_sdk/pydantic/insights_repository_project_collection.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/engineering-insights/repositories/projects` `put`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.insights_repositories_(beta).list_repositories`<a id="launchdarklyinsights_repositories_betalist_repositories"></a>

Get a list of repositories

### Expanding the repository collection response<a id="expanding-the-repository-collection-response"></a>

LaunchDarkly supports expanding the repository collection response to include additional fields.

To expand the response, append the `expand` query parameter and include the following:

* `projects` includes details on all of the LaunchDarkly projects associated with each repository

For example, use `?expand=projects` to include the `projects` field in the response. By default, this field is **not** included in the response.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_repositories_response = launchdarkly.insights_repositories_(beta).list_repositories(
    expand="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### expand: `str`<a id="expand-str"></a>

Expand properties in response. Options: `projects`

#### 🔄 Return<a id="🔄-return"></a>

[`InsightsRepositoryCollection`](./launch_darkly_python_sdk/pydantic/insights_repository_collection.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/engineering-insights/repositories` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.insights_repositories_(beta).remove_repository_project_association`<a id="launchdarklyinsights_repositories_betaremove_repository_project_association"></a>

Remove repository project association

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
launchdarkly.insights_repositories_(beta).remove_repository_project_association(
    repository_key="repositoryKey_example",
    project_key="projectKey_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### repository_key: `str`<a id="repository_key-str"></a>

The repository key

##### project_key: `str`<a id="project_key-str"></a>

The project key

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/engineering-insights/repositories/{repositoryKey}/projects/{projectKey}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.insights_scores_(beta).create_insight_group`<a id="launchdarklyinsights_scores_betacreate_insight_group"></a>

Create insight group

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
create_insight_group_response = launchdarkly.insights_scores_(beta).create_insight_group(
    name="Production - All Apps",
    key="default-production-all-apps",
    project_key="default",
    environment_key="production",
    application_keys=["billing-service", "inventory-service"],
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### name: `str`<a id="name-str"></a>

The name of the insight group

##### key: `str`<a id="key-str"></a>

The key of the insight group

##### project_key: `str`<a id="project_key-str"></a>

The projectKey to be associated with the insight group

##### environment_key: `str`<a id="environment_key-str"></a>

The environmentKey to be associated with the insight group

##### application_keys: [`PostInsightGroupParamsApplicationKeys`](./launch_darkly_python_sdk/type/post_insight_group_params_application_keys.py)<a id="application_keys-postinsightgroupparamsapplicationkeyslaunch_darkly_python_sdktypepost_insight_group_params_application_keyspy"></a>

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`PostInsightGroupParams`](./launch_darkly_python_sdk/type/post_insight_group_params.py)
#### 🔄 Return<a id="🔄-return"></a>

[`InsightGroup`](./launch_darkly_python_sdk/pydantic/insight_group.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/engineering-insights/insights/group` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.insights_scores_(beta).delete_insight_group`<a id="launchdarklyinsights_scores_betadelete_insight_group"></a>

Delete insight group

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
launchdarkly.insights_scores_(beta).delete_insight_group(
    insight_group_key="insightGroupKey_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### insight_group_key: `str`<a id="insight_group_key-str"></a>

The insight group key

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/engineering-insights/insights/groups/{insightGroupKey}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.insights_scores_(beta).expand_group_insight_scores`<a id="launchdarklyinsights_scores_betaexpand_group_insight_scores"></a>

Get insight group

### Expanding the insight group response<a id="expanding-the-insight-group-response"></a>

LaunchDarkly supports expanding the insight group response to include additional fields.

To expand the response, append the `expand` query parameter and include the following:

* `scores` includes details on all of the scores used in the engineering insights metrics views for this group
* `environment` includes details on each environment associated with this group

For example, use `?expand=scores` to include the `scores` field in the response. By default, this field is **not** included in the response.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
expand_group_insight_scores_response = launchdarkly.insights_scores_(beta).expand_group_insight_scores(
    insight_group_key="insightGroupKey_example",
    expand="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### insight_group_key: `str`<a id="insight_group_key-str"></a>

The insight group key

##### expand: `str`<a id="expand-str"></a>

Options: `scores`, `environment`

#### 🔄 Return<a id="🔄-return"></a>

[`InsightGroup`](./launch_darkly_python_sdk/pydantic/insight_group.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/engineering-insights/insights/groups/{insightGroupKey}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.insights_scores_(beta).get_insight_scores`<a id="launchdarklyinsights_scores_betaget_insight_scores"></a>

Return insights scores, based on the given parameters. This data is also used in engineering insights metrics views.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_insight_scores_response = launchdarkly.insights_scores_(beta).get_insight_scores(
    project_key="projectKey_example",
    environment_key="environmentKey_example",
    application_key="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

##### application_key: `str`<a id="application_key-str"></a>

Comma separated list of application keys

#### 🔄 Return<a id="🔄-return"></a>

[`InsightScores`](./launch_darkly_python_sdk/pydantic/insight_scores.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/engineering-insights/insights/scores` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.insights_scores_(beta).list_group_insight_scores`<a id="launchdarklyinsights_scores_betalist_group_insight_scores"></a>

List groups for which you are collecting insights

### Expanding the insight groups collection response<a id="expanding-the-insight-groups-collection-response"></a>

LaunchDarkly supports expanding the insight groups collection response to include additional fields.

To expand the response, append the `expand` query parameter and include the following:

* `scores` includes details on all of the scores used in the engineering insights metrics views for each group
* `environment` includes details on each environment associated with each group
* `metadata` includes counts of the number of insight groups with particular indicators, such as "execellent," "good," "fair," and so on.

For example, use `?expand=scores` to include the `scores` field in the response. By default, this field is **not** included in the response.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_group_insight_scores_response = launchdarkly.insights_scores_(beta).list_group_insight_scores(
    limit=1,
    offset=1,
    sort="string_example",
    query="string_example",
    expand="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### limit: `int`<a id="limit-int"></a>

The number of insight groups to return. Default is 20. Must be between 1 and 20 inclusive.

##### offset: `int`<a id="offset-int"></a>

Where to start in the list. Use this with pagination. For example, an offset of 10 skips the first ten items and then returns the next items in the list, up to the query `limit`.

##### sort: `str`<a id="sort-str"></a>

Sort flag list by field. Prefix field with <code>-</code> to sort in descending order. Allowed fields: name

##### query: `str`<a id="query-str"></a>

Filter list of insights groups by name.

##### expand: `str`<a id="expand-str"></a>

Options: `scores`, `environment`, `metadata`

#### 🔄 Return<a id="🔄-return"></a>

[`InsightGroupCollection`](./launch_darkly_python_sdk/pydantic/insight_group_collection.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/engineering-insights/insights/groups` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.insights_scores_(beta).update_insight_group_patch`<a id="launchdarklyinsights_scores_betaupdate_insight_group_patch"></a>

Update an insight group. Updating an insight group uses a [JSON patch](https://datatracker.ietf.org/doc/html/rfc6902) representation of the desired changes. To learn more, read [Updates](https://apidocs.launchdarkly.com).

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
update_insight_group_patch_response = launchdarkly.insights_scores_(beta).update_insight_group_patch(
    body=[{"op":"replace","path":"/name","value":"Prod group"}],
    insight_group_key="insightGroupKey_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### insight_group_key: `str`<a id="insight_group_key-str"></a>

The insight group key

##### requestBody: [`JSONPatch`](./launch_darkly_python_sdk/type/json_patch.py)<a id="requestbody-jsonpatchlaunch_darkly_python_sdktypejson_patchpy"></a>

#### 🔄 Return<a id="🔄-return"></a>

[`InsightGroup`](./launch_darkly_python_sdk/pydantic/insight_group.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/engineering-insights/insights/groups/{insightGroupKey}` `patch`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.integration_audit_log_subscriptions.create_subscription`<a id="launchdarklyintegration_audit_log_subscriptionscreate_subscription"></a>

Create an audit log subscription.<br /><br />For each subscription, you must specify the set of resources you wish to subscribe to audit log notifications for. You can describe these resources using a custom role policy. To learn more, read [Custom role concepts](https://docs.launchdarkly.com/home/members/role-concepts).

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
create_subscription_response = launchdarkly.integration_audit_log_subscriptions.create_subscription(
    name="Example audit log subscription.",
    config={
        "key": None,
    },
    integration_key="integrationKey_example",
    tags=["testing-tag"],
    statements=[
        {
            "resources": ["proj/*:env/*:flag/*;testing-tag"],
            "actions": ["*"],
            "effect": "allow",
        }
    ],
    _true=False,
    url="string_example",
    api_key="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### name: `str`<a id="name-str"></a>

A human-friendly name for your audit log subscription.

##### config: [`SubscriptionPostConfig`](./launch_darkly_python_sdk/type/subscription_post_config.py)<a id="config-subscriptionpostconfiglaunch_darkly_python_sdktypesubscription_post_configpy"></a>

##### integration_key: `str`<a id="integration_key-str"></a>

The integration key

##### tags: [`SubscriptionPostTags`](./launch_darkly_python_sdk/type/subscription_post_tags.py)<a id="tags-subscriptionposttagslaunch_darkly_python_sdktypesubscription_post_tagspy"></a>

##### statements: [`StatementPostList`](./launch_darkly_python_sdk/type/statement_post_list.py)<a id="statements-statementpostlistlaunch_darkly_python_sdktypestatement_post_listpy"></a>

##### _true: `bool`<a id="_true-bool"></a>

Whether or not you want your subscription to actively send events.

##### url: `str`<a id="url-str"></a>

Slack webhook receiver URL. Only necessary for legacy Slack webhook integrations.

##### api_key: `str`<a id="api_key-str"></a>

Datadog API key. Only necessary for legacy Datadog webhook integrations.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`SubscriptionPost`](./launch_darkly_python_sdk/type/subscription_post.py)
#### 🔄 Return<a id="🔄-return"></a>

[`Integration`](./launch_darkly_python_sdk/pydantic/integration.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/integrations/{integrationKey}` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.integration_audit_log_subscriptions.delete_subscription`<a id="launchdarklyintegration_audit_log_subscriptionsdelete_subscription"></a>

Delete an audit log subscription.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
launchdarkly.integration_audit_log_subscriptions.delete_subscription(
    integration_key="integrationKey_example",
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### integration_key: `str`<a id="integration_key-str"></a>

The integration key

##### id: `str`<a id="id-str"></a>

The subscription ID

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/integrations/{integrationKey}/{id}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.integration_audit_log_subscriptions.get_by_id`<a id="launchdarklyintegration_audit_log_subscriptionsget_by_id"></a>

Get an audit log subscription by ID.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_by_id_response = launchdarkly.integration_audit_log_subscriptions.get_by_id(
    integration_key="integrationKey_example",
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### integration_key: `str`<a id="integration_key-str"></a>

The integration key

##### id: `str`<a id="id-str"></a>

The subscription ID

#### 🔄 Return<a id="🔄-return"></a>

[`Integration`](./launch_darkly_python_sdk/pydantic/integration.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/integrations/{integrationKey}/{id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.integration_audit_log_subscriptions.list_by_integration`<a id="launchdarklyintegration_audit_log_subscriptionslist_by_integration"></a>

Get all audit log subscriptions associated with a given integration.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_by_integration_response = launchdarkly.integration_audit_log_subscriptions.list_by_integration(
    integration_key="integrationKey_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### integration_key: `str`<a id="integration_key-str"></a>

The integration key

#### 🔄 Return<a id="🔄-return"></a>

[`Integrations`](./launch_darkly_python_sdk/pydantic/integrations.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/integrations/{integrationKey}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.integration_audit_log_subscriptions.update_subscription`<a id="launchdarklyintegration_audit_log_subscriptionsupdate_subscription"></a>

Update an audit log subscription configuration. Updating an audit log subscription uses a [JSON patch](https://datatracker.ietf.org/doc/html/rfc6902) representation of the desired changes. To learn more, read [Updates](https://apidocs.launchdarkly.com).

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
update_subscription_response = launchdarkly.integration_audit_log_subscriptions.update_subscription(
    body=[{"op":"replace","path":"/on","value":false}],
    integration_key="integrationKey_example",
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### integration_key: `str`<a id="integration_key-str"></a>

The integration key

##### id: `str`<a id="id-str"></a>

The ID of the audit log subscription

##### requestBody: [`JSONPatch`](./launch_darkly_python_sdk/type/json_patch.py)<a id="requestbody-jsonpatchlaunch_darkly_python_sdktypejson_patchpy"></a>

#### 🔄 Return<a id="🔄-return"></a>

[`Integration`](./launch_darkly_python_sdk/pydantic/integration.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/integrations/{integrationKey}/{id}` `patch`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.integration_delivery_configurations_(beta).create_delivery_configuration`<a id="launchdarklyintegration_delivery_configurations_betacreate_delivery_configuration"></a>

Create a delivery configuration.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
create_delivery_configuration_response = launchdarkly.integration_delivery_configurations_(beta).create_delivery_configuration(
    config={
        "key": None,
    },
    project_key="projectKey_example",
    environment_key="environmentKey_example",
    integration_key="integrationKey_example",
    tags=["example-tag"],
    _true=False,
    name="Sample integration",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### config: [`FormVariableConfig`](./launch_darkly_python_sdk/type/form_variable_config.py)<a id="config-formvariableconfiglaunch_darkly_python_sdktypeform_variable_configpy"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

##### integration_key: `str`<a id="integration_key-str"></a>

The integration key

##### tags: [`IntegrationDeliveryConfigurationPostTags`](./launch_darkly_python_sdk/type/integration_delivery_configuration_post_tags.py)<a id="tags-integrationdeliveryconfigurationposttagslaunch_darkly_python_sdktypeintegration_delivery_configuration_post_tagspy"></a>

##### _true: `bool`<a id="_true-bool"></a>

Whether the integration configuration is active. Default value is false.

##### name: `str`<a id="name-str"></a>

Name to identify the integration

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`IntegrationDeliveryConfigurationPost`](./launch_darkly_python_sdk/type/integration_delivery_configuration_post.py)
#### 🔄 Return<a id="🔄-return"></a>

[`IntegrationDeliveryConfiguration`](./launch_darkly_python_sdk/pydantic/integration_delivery_configuration.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/integration-capabilities/featureStore/{projectKey}/{environmentKey}/{integrationKey}` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.integration_delivery_configurations_(beta).delete_delivery_configuration`<a id="launchdarklyintegration_delivery_configurations_betadelete_delivery_configuration"></a>

Delete a delivery configuration.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
launchdarkly.integration_delivery_configurations_(beta).delete_delivery_configuration(
    project_key="projectKey_example",
    environment_key="environmentKey_example",
    integration_key="integrationKey_example",
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

##### integration_key: `str`<a id="integration_key-str"></a>

The integration key

##### id: `str`<a id="id-str"></a>

The configuration ID

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/integration-capabilities/featureStore/{projectKey}/{environmentKey}/{integrationKey}/{id}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.integration_delivery_configurations_(beta).get_by_id`<a id="launchdarklyintegration_delivery_configurations_betaget_by_id"></a>

Get delivery configuration by ID.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_by_id_response = launchdarkly.integration_delivery_configurations_(beta).get_by_id(
    project_key="projectKey_example",
    environment_key="environmentKey_example",
    integration_key="integrationKey_example",
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

##### integration_key: `str`<a id="integration_key-str"></a>

The integration key

##### id: `str`<a id="id-str"></a>

The configuration ID

#### 🔄 Return<a id="🔄-return"></a>

[`IntegrationDeliveryConfiguration`](./launch_darkly_python_sdk/pydantic/integration_delivery_configuration.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/integration-capabilities/featureStore/{projectKey}/{environmentKey}/{integrationKey}/{id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.integration_delivery_configurations_(beta).get_delivery_configurations_by_environment`<a id="launchdarklyintegration_delivery_configurations_betaget_delivery_configurations_by_environment"></a>

Get delivery configurations by environment.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_delivery_configurations_by_environment_response = launchdarkly.integration_delivery_configurations_(beta).get_delivery_configurations_by_environment(
    project_key="projectKey_example",
    environment_key="environmentKey_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

#### 🔄 Return<a id="🔄-return"></a>

[`IntegrationDeliveryConfigurationCollection`](./launch_darkly_python_sdk/pydantic/integration_delivery_configuration_collection.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/integration-capabilities/featureStore/{projectKey}/{environmentKey}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.integration_delivery_configurations_(beta).list_delivery_configurations`<a id="launchdarklyintegration_delivery_configurations_betalist_delivery_configurations"></a>

List all delivery configurations.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_delivery_configurations_response = launchdarkly.integration_delivery_configurations_(beta).list_delivery_configurations()
```

#### 🔄 Return<a id="🔄-return"></a>

[`IntegrationDeliveryConfigurationCollection`](./launch_darkly_python_sdk/pydantic/integration_delivery_configuration_collection.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/integration-capabilities/featureStore` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.integration_delivery_configurations_(beta).update_delivery_configuration`<a id="launchdarklyintegration_delivery_configurations_betaupdate_delivery_configuration"></a>

Update an integration delivery configuration. Updating an integration delivery configuration uses a [JSON patch](https://datatracker.ietf.org/doc/html/rfc6902) representation of the desired changes. To learn more, read [Updates](https://apidocs.launchdarkly.com).

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
update_delivery_configuration_response = launchdarkly.integration_delivery_configurations_(beta).update_delivery_configuration(
    body=[{"op":"replace","path":"/on","value":true}],
    project_key="projectKey_example",
    environment_key="environmentKey_example",
    integration_key="integrationKey_example",
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

##### integration_key: `str`<a id="integration_key-str"></a>

The integration key

##### id: `str`<a id="id-str"></a>

The configuration ID

##### requestBody: [`JSONPatch`](./launch_darkly_python_sdk/type/json_patch.py)<a id="requestbody-jsonpatchlaunch_darkly_python_sdktypejson_patchpy"></a>

#### 🔄 Return<a id="🔄-return"></a>

[`IntegrationDeliveryConfiguration`](./launch_darkly_python_sdk/pydantic/integration_delivery_configuration.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/integration-capabilities/featureStore/{projectKey}/{environmentKey}/{integrationKey}/{id}` `patch`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.integration_delivery_configurations_(beta).validate_delivery_configuration`<a id="launchdarklyintegration_delivery_configurations_betavalidate_delivery_configuration"></a>

Validate the saved delivery configuration, using the `validationRequest` in the integration's `manifest.json` file.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
validate_delivery_configuration_response = launchdarkly.integration_delivery_configurations_(beta).validate_delivery_configuration(
    project_key="projectKey_example",
    environment_key="environmentKey_example",
    integration_key="integrationKey_example",
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

##### integration_key: `str`<a id="integration_key-str"></a>

The integration key

##### id: `str`<a id="id-str"></a>

The configuration ID

#### 🔄 Return<a id="🔄-return"></a>

[`IntegrationDeliveryConfigurationResponse`](./launch_darkly_python_sdk/pydantic/integration_delivery_configuration_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/integration-capabilities/featureStore/{projectKey}/{environmentKey}/{integrationKey}/{id}/validate` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.integrations_(beta).create_persistent_store_integration`<a id="launchdarklyintegrations_betacreate_persistent_store_integration"></a>


Create a persistent store integration.

If you are using server-side SDKs, segments synced from external tools and larger list-based segments require a persistent store within your infrastructure. LaunchDarkly keeps the persistent store up to date and consults it during flag evaluation.

You can use either Redis or DynamoDB as your persistent store. When you create a persistent store integration, the fields in the `config` object in the request vary depending on which persistent store you use.

If you are using Redis to create your persistent store integration, you will need to know:

* Your Redis host
* Your Redis port
* Your Redis username
* Your Redis password
* Whether or not LaunchDarkly should connect using TLS

If you are using DynamoDB to create your persistent store integration, you will need to know:

* Your DynamoDB table name. The table must have the following schema:
  * Partition key: `namespace` (string)
  * Sort key: `key` (string)
* Your DynamoDB Amazon Web Services (AWS) region.
* Your AWS role Amazon Resource Name (ARN). This is the role that LaunchDarkly will assume to manage your DynamoDB table.
* The External ID you specified when creating your Amazon Resource Name (ARN).

To learn more, read [Segment configuration](https://docs.launchdarkly.com/home/segments/big-segment-configuration).


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
create_persistent_store_integration_response = launchdarkly.integrations_(beta).create_persistent_store_integration(
    config={
        "key": None,
    },
    project_key="projectKey_example",
    environment_key="environmentKey_example",
    integration_key="integrationKey_example",
    tags=["example-tag"],
    _true=False,
    name="Sample integration",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### config: [`FormVariableConfig`](./launch_darkly_python_sdk/type/form_variable_config.py)<a id="config-formvariableconfiglaunch_darkly_python_sdktypeform_variable_configpy"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

##### integration_key: `str`<a id="integration_key-str"></a>

The integration key, either `redis` or `dynamodb`

##### tags: [`IntegrationDeliveryConfigurationPostTags`](./launch_darkly_python_sdk/type/integration_delivery_configuration_post_tags.py)<a id="tags-integrationdeliveryconfigurationposttagslaunch_darkly_python_sdktypeintegration_delivery_configuration_post_tagspy"></a>

##### _true: `bool`<a id="_true-bool"></a>

Whether the integration configuration is active. Default value is false.

##### name: `str`<a id="name-str"></a>

Name to identify the integration

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`IntegrationDeliveryConfigurationPost`](./launch_darkly_python_sdk/type/integration_delivery_configuration_post.py)
#### 🔄 Return<a id="🔄-return"></a>

[`BigSegmentStoreIntegration`](./launch_darkly_python_sdk/pydantic/big_segment_store_integration.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/integration-capabilities/big-segment-store/{projectKey}/{environmentKey}/{integrationKey}` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.integrations_(beta).delete_big_segment_store_integration`<a id="launchdarklyintegrations_betadelete_big_segment_store_integration"></a>

Delete a persistent store integration. Each integration uses either Redis or DynamoDB.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
launchdarkly.integrations_(beta).delete_big_segment_store_integration(
    project_key="projectKey_example",
    environment_key="environmentKey_example",
    integration_key="integrationKey_example",
    integration_id="integrationId_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

##### integration_key: `str`<a id="integration_key-str"></a>

The integration key, either `redis` or `dynamodb`

##### integration_id: `str`<a id="integration_id-str"></a>

The integration ID

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/integration-capabilities/big-segment-store/{projectKey}/{environmentKey}/{integrationKey}/{integrationId}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.integrations_(beta).get_big_segment_store_integration_by_id`<a id="launchdarklyintegrations_betaget_big_segment_store_integration_by_id"></a>

Get a big segment store integration by ID.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_big_segment_store_integration_by_id_response = launchdarkly.integrations_(beta).get_big_segment_store_integration_by_id(
    project_key="projectKey_example",
    environment_key="environmentKey_example",
    integration_key="integrationKey_example",
    integration_id="integrationId_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

##### integration_key: `str`<a id="integration_key-str"></a>

The integration key, either `redis` or `dynamodb`

##### integration_id: `str`<a id="integration_id-str"></a>

The integration ID

#### 🔄 Return<a id="🔄-return"></a>

[`BigSegmentStoreIntegration`](./launch_darkly_python_sdk/pydantic/big_segment_store_integration.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/integration-capabilities/big-segment-store/{projectKey}/{environmentKey}/{integrationKey}/{integrationId}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.integrations_(beta).list_big_segment_store_integrations`<a id="launchdarklyintegrations_betalist_big_segment_store_integrations"></a>

List all big segment store integrations.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_big_segment_store_integrations_response = launchdarkly.integrations_(beta).list_big_segment_store_integrations()
```

#### 🔄 Return<a id="🔄-return"></a>

[`BigSegmentStoreIntegrationCollection`](./launch_darkly_python_sdk/pydantic/big_segment_store_integration_collection.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/integration-capabilities/big-segment-store` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.integrations_(beta).update_big_segment_store`<a id="launchdarklyintegrations_betaupdate_big_segment_store"></a>

Update a big segment store integration. Updating a big segment store requires a [JSON Patch](https://datatracker.ietf.org/doc/html/rfc6902) representation of the desired changes. To learn more, read [Updates](https://apidocs.launchdarkly.com).

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
update_big_segment_store_response = launchdarkly.integrations_(beta).update_big_segment_store(
    body=[
        {
            "op": "replace",
            "path": "/exampleField",
            "value": None,
        }
    ],
    project_key="projectKey_example",
    environment_key="environmentKey_example",
    integration_key="integrationKey_example",
    integration_id="integrationId_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

##### integration_key: `str`<a id="integration_key-str"></a>

The integration key, either `redis` or `dynamodb`

##### integration_id: `str`<a id="integration_id-str"></a>

The integration ID

##### requestBody: [`JSONPatch`](./launch_darkly_python_sdk/type/json_patch.py)<a id="requestbody-jsonpatchlaunch_darkly_python_sdktypejson_patchpy"></a>

#### 🔄 Return<a id="🔄-return"></a>

[`BigSegmentStoreIntegration`](./launch_darkly_python_sdk/pydantic/big_segment_store_integration.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/integration-capabilities/big-segment-store/{projectKey}/{environmentKey}/{integrationKey}/{integrationId}` `patch`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.metrics.create_new_metric`<a id="launchdarklymetricscreate_new_metric"></a>

Create a new metric in the specified project. The expected `POST` body differs depending on the specified `kind` property.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
create_new_metric_response = launchdarkly.metrics.create_new_metric(
    key="metric-key-123abc",
    kind="custom",
    project_key="projectKey_example",
    tags=["example-tag"],
    description="optional description",
    name="Example metric",
    selector=".dropdown-toggle",
    urls=[
        {
            "kind": "exact",
        }
    ],
    is_active=True,
    is_numeric=False,
    unit="orders",
    event_key="sales generated",
    success_criteria="HigherThanBaseline",
    randomization_units=["user"],
    unit_aggregation_type="average",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### key: `str`<a id="key-str"></a>

A unique key to reference the metric

##### kind: `str`<a id="kind-str"></a>

The kind of event your metric will track

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### tags: [`MetricPostTags`](./launch_darkly_python_sdk/type/metric_post_tags.py)<a id="tags-metricposttagslaunch_darkly_python_sdktypemetric_post_tagspy"></a>

##### description: `str`<a id="description-str"></a>

Description of the metric

##### name: `str`<a id="name-str"></a>

A human-friendly name for the metric

##### selector: `str`<a id="selector-str"></a>

One or more CSS selectors. Required for click metrics only.

##### urls: List[`UrlPost`]<a id="urls-listurlpost"></a>

One or more target URLs. Required for click and pageview metrics only.

##### is_active: `bool`<a id="is_active-bool"></a>

Whether the metric is active. Set to <code>true</code> to record click or pageview metrics. Not applicable for custom metrics.

##### is_numeric: `bool`<a id="is_numeric-bool"></a>

Whether to track numeric changes in value against a baseline (<code>true</code>) or to track a conversion when an end user takes an action (<code>false</code>). Required for custom metrics only.

##### unit: `str`<a id="unit-str"></a>

The unit of measure. Applicable for numeric custom metrics only.

##### event_key: `str`<a id="event_key-str"></a>

The event key to use in your code. Required for custom conversion/binary and custom numeric metrics only.

##### success_criteria: `str`<a id="success_criteria-str"></a>

Success criteria. Required for custom numeric metrics, optional for custom conversion metrics.

##### randomization_units: [`MetricPostRandomizationUnits`](./launch_darkly_python_sdk/type/metric_post_randomization_units.py)<a id="randomization_units-metricpostrandomizationunitslaunch_darkly_python_sdktypemetric_post_randomization_unitspy"></a>

##### unit_aggregation_type: `str`<a id="unit_aggregation_type-str"></a>

The method in which multiple unit event values are aggregated

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`MetricPost`](./launch_darkly_python_sdk/type/metric_post.py)
#### 🔄 Return<a id="🔄-return"></a>

[`MetricRep`](./launch_darkly_python_sdk/pydantic/metric_rep.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/metrics/{projectKey}` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.metrics.delete_by_project_and_metric_key`<a id="launchdarklymetricsdelete_by_project_and_metric_key"></a>

Delete a metric by key.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
launchdarkly.metrics.delete_by_project_and_metric_key(
    project_key="projectKey_example",
    metric_key="metricKey_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### metric_key: `str`<a id="metric_key-str"></a>

The metric key

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/metrics/{projectKey}/{metricKey}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.metrics.get_single_metric`<a id="launchdarklymetricsget_single_metric"></a>

Get information for a single metric from the specific project.

### Expanding the metric response<a id="expanding-the-metric-response"></a>
LaunchDarkly supports four fields for expanding the "Get metric" response. By default, these fields are **not** included in the response.

To expand the response, append the `expand` query parameter and add a comma-separated list with any of the following fields:

- `experiments` includes all experiments from the specific project that use the metric
- `experimentCount` includes the number of experiments from the specific project that use the metric
- `metricGroups` includes all metric groups from the specific project that use the metric
- `metricGroupCount` includes the number of metric groups from the specific project that use the metric

For example, `expand=experiments` includes the `experiments` field in the response.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_single_metric_response = launchdarkly.metrics.get_single_metric(
    project_key="projectKey_example",
    metric_key="metricKey_example",
    expand="string_example",
    version_id="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### metric_key: `str`<a id="metric_key-str"></a>

The metric key

##### expand: `str`<a id="expand-str"></a>

A comma-separated list of properties that can reveal additional information in the response.

##### version_id: `str`<a id="version_id-str"></a>

The specific version ID of the metric

#### 🔄 Return<a id="🔄-return"></a>

[`MetricRep`](./launch_darkly_python_sdk/pydantic/metric_rep.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/metrics/{projectKey}/{metricKey}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.metrics.list_for_project`<a id="launchdarklymetricslist_for_project"></a>

Get a list of all metrics for the specified project.

### Expanding the metric list response<a id="expanding-the-metric-list-response"></a>
LaunchDarkly supports expanding the "List metrics" response. By default, the expandable field is **not** included in the response.

To expand the response, append the `expand` query parameter and add the following supported field:

- `experimentCount` includes the number of experiments from the specific project that use the metric

For example, `expand=experimentCount` includes the `experimentCount` field for each metric in the response.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_for_project_response = launchdarkly.metrics.list_for_project(
    project_key="projectKey_example",
    expand="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### expand: `str`<a id="expand-str"></a>

A comma-separated list of properties that can reveal additional information in the response.

#### 🔄 Return<a id="🔄-return"></a>

[`MetricCollectionRep`](./launch_darkly_python_sdk/pydantic/metric_collection_rep.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/metrics/{projectKey}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.metrics.update_by_json_patch`<a id="launchdarklymetricsupdate_by_json_patch"></a>

Patch a metric by key. Updating a metric uses a [JSON patch](https://datatracker.ietf.org/doc/html/rfc6902) representation of the desired changes. To learn more, read [Updates](https://apidocs.launchdarkly.com).

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
update_by_json_patch_response = launchdarkly.metrics.update_by_json_patch(
    body=[{"op":"replace","path":"/name","value":"my-updated-metric"}],
    project_key="projectKey_example",
    metric_key="metricKey_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### metric_key: `str`<a id="metric_key-str"></a>

The metric key

##### requestBody: [`JSONPatch`](./launch_darkly_python_sdk/type/json_patch.py)<a id="requestbody-jsonpatchlaunch_darkly_python_sdktypejson_patchpy"></a>

#### 🔄 Return<a id="🔄-return"></a>

[`MetricRep`](./launch_darkly_python_sdk/pydantic/metric_rep.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/metrics/{projectKey}/{metricKey}` `patch`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.metrics_(beta).create_metric_group`<a id="launchdarklymetrics_betacreate_metric_group"></a>

Create a new metric group in the specified project

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
create_metric_group_response = launchdarkly.metrics_(beta).create_metric_group(
    tags=["ops"],
    key="metric-group-key-123abc",
    name="My metric group",
    kind="funnel",
    maintainer_id="569fdeadbeef1644facecafe",
    metrics=[
        {
            "key": "metric-key-123abc",
            "name_in_group": "Step 1",
        }
    ],
    project_key="projectKey_example",
    description="Description of the metric group",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### tags: [`MetricGroupPostTags`](./launch_darkly_python_sdk/type/metric_group_post_tags.py)<a id="tags-metricgroupposttagslaunch_darkly_python_sdktypemetric_group_post_tagspy"></a>

##### key: `str`<a id="key-str"></a>

A unique key to reference the metric group

##### name: `str`<a id="name-str"></a>

A human-friendly name for the metric group

##### kind: `str`<a id="kind-str"></a>

The type of the metric group

##### maintainer_id: `str`<a id="maintainer_id-str"></a>

The ID of the member who maintains this metric group

##### metrics: List[`MetricInMetricGroupInput`]<a id="metrics-listmetricinmetricgroupinput"></a>

An ordered list of the metrics in this metric group

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### description: `str`<a id="description-str"></a>

Description of the metric group

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`MetricGroupPost`](./launch_darkly_python_sdk/type/metric_group_post.py)
#### 🔄 Return<a id="🔄-return"></a>

[`MetricGroupRep`](./launch_darkly_python_sdk/pydantic/metric_group_rep.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/projects/{projectKey}/metric-groups` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.metrics_(beta).delete_metric_group`<a id="launchdarklymetrics_betadelete_metric_group"></a>

Delete a metric group by key.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
launchdarkly.metrics_(beta).delete_metric_group(
    project_key="projectKey_example",
    metric_group_key="metricGroupKey_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### metric_group_key: `str`<a id="metric_group_key-str"></a>

The metric group key

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/projects/{projectKey}/metric-groups/{metricGroupKey}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.metrics_(beta).get_metric_group_details`<a id="launchdarklymetrics_betaget_metric_group_details"></a>

Get information for a single metric group from the specific project.

### Expanding the metric group response<a id="expanding-the-metric-group-response"></a>
LaunchDarkly supports two fields for expanding the "Get metric group" response. By default, these fields are **not** included in the response.

To expand the response, append the `expand` query parameter and add a comma-separated list with either or both of the following fields:

- `experiments` includes all experiments from the specific project that use the metric group
- `experimentCount` includes the number of experiments from the specific project that use the metric group

For example, `expand=experiments` includes the `experiments` field in the response.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_metric_group_details_response = launchdarkly.metrics_(beta).get_metric_group_details(
    project_key="projectKey_example",
    metric_group_key="metricGroupKey_example",
    expand="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### metric_group_key: `str`<a id="metric_group_key-str"></a>

The metric group key

##### expand: `str`<a id="expand-str"></a>

A comma-separated list of properties that can reveal additional information in the response.

#### 🔄 Return<a id="🔄-return"></a>

[`MetricGroupRep`](./launch_darkly_python_sdk/pydantic/metric_group_rep.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/projects/{projectKey}/metric-groups/{metricGroupKey}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.metrics_(beta).list_metric_groups`<a id="launchdarklymetrics_betalist_metric_groups"></a>

Get a list of all metric groups for the specified project.

### Expanding the metric groups response<a id="expanding-the-metric-groups-response"></a>
LaunchDarkly supports one field for expanding the "Get metric groups" response. By default, these fields are **not** included in the response.

To expand the response, append the `expand` query parameter and add a comma-separated list with the following field:

- `experiments` includes all experiments from the specific project that use the metric group

For example, `expand=experiments` includes the `experiments` field in the response.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_metric_groups_response = launchdarkly.metrics_(beta).list_metric_groups(
    project_key="projectKey_example",
    expand="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### expand: `str`<a id="expand-str"></a>

A comma-separated list of properties that can reveal additional information in the response.

#### 🔄 Return<a id="🔄-return"></a>

[`MetricGroupCollectionRep`](./launch_darkly_python_sdk/pydantic/metric_group_collection_rep.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/projects/{projectKey}/metric-groups` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.metrics_(beta).update_metric_group_by_key`<a id="launchdarklymetrics_betaupdate_metric_group_by_key"></a>

Patch a metric group by key. Updating a metric group uses a [JSON patch](https://datatracker.ietf.org/doc/html/rfc6902) representation of the desired changes.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
update_metric_group_by_key_response = launchdarkly.metrics_(beta).update_metric_group_by_key(
    body=[{"op":"replace","path":"/name","value":"my-updated-metric-group"}],
    project_key="projectKey_example",
    metric_group_key="metricGroupKey_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### metric_group_key: `str`<a id="metric_group_key-str"></a>

The metric group key

##### requestBody: [`JSONPatch`](./launch_darkly_python_sdk/type/json_patch.py)<a id="requestbody-jsonpatchlaunch_darkly_python_sdktypejson_patchpy"></a>

#### 🔄 Return<a id="🔄-return"></a>

[`MetricGroupRep`](./launch_darkly_python_sdk/pydantic/metric_group_rep.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/projects/{projectKey}/metric-groups/{metricGroupKey}` `patch`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.o_auth2_clients.create_client`<a id="launchdarklyo_auth2_clientscreate_client"></a>

Create (register) a LaunchDarkly OAuth2 client. OAuth2 clients allow you to build custom integrations using LaunchDarkly as your identity provider.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
create_client_response = launchdarkly.o_auth2_clients.create_client(
    description="string_example",
    name="string_example",
    redirect_uri="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### description: `str`<a id="description-str"></a>

Description of your OAuth 2.0 client.

##### name: `str`<a id="name-str"></a>

The name of your new LaunchDarkly OAuth 2.0 client.

##### redirect_uri: `str`<a id="redirect_uri-str"></a>

The redirect URI for your new OAuth 2.0 application. This should be an absolute URL conforming with the standard HTTPS protocol.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`OauthClientPost`](./launch_darkly_python_sdk/type/oauth_client_post.py)
#### 🔄 Return<a id="🔄-return"></a>

[`Client`](./launch_darkly_python_sdk/pydantic/client.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/oauth/clients` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.o_auth2_clients.delete_client_by_id`<a id="launchdarklyo_auth2_clientsdelete_client_by_id"></a>

Delete an existing OAuth 2.0 client by unique client ID.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
launchdarkly.o_auth2_clients.delete_client_by_id(
    client_id="clientId_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### client_id: `str`<a id="client_id-str"></a>

The client ID

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/oauth/clients/{clientId}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.o_auth2_clients.get_client_by_id`<a id="launchdarklyo_auth2_clientsget_client_by_id"></a>

Get a registered OAuth 2.0 client by unique client ID.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_client_by_id_response = launchdarkly.o_auth2_clients.get_client_by_id(
    client_id="clientId_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### client_id: `str`<a id="client_id-str"></a>

The client ID

#### 🔄 Return<a id="🔄-return"></a>

[`Client`](./launch_darkly_python_sdk/pydantic/client.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/oauth/clients/{clientId}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.o_auth2_clients.list`<a id="launchdarklyo_auth2_clientslist"></a>

Get all OAuth 2.0 clients registered by your account.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_response = launchdarkly.o_auth2_clients.list()
```

#### 🔄 Return<a id="🔄-return"></a>

[`ClientCollection`](./launch_darkly_python_sdk/pydantic/client_collection.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/oauth/clients` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.o_auth2_clients.update_client_by_id`<a id="launchdarklyo_auth2_clientsupdate_client_by_id"></a>

Patch an existing OAuth 2.0 client by client ID. Updating an OAuth2 client uses a [JSON patch](https://datatracker.ietf.org/doc/html/rfc6902) representation of the desired changes. To learn more, read [Updates](https://apidocs.launchdarkly.com). Only `name`, `description`, and `redirectUri` may be patched.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
update_client_by_id_response = launchdarkly.o_auth2_clients.update_client_by_id(
    body=[{"op":"replace","path":"/name","value":"Example Client V2"}],
    client_id="clientId_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### client_id: `str`<a id="client_id-str"></a>

The client ID

##### requestBody: [`JSONPatch`](./launch_darkly_python_sdk/type/json_patch.py)<a id="requestbody-jsonpatchlaunch_darkly_python_sdktypejson_patchpy"></a>

#### 🔄 Return<a id="🔄-return"></a>

[`Client`](./launch_darkly_python_sdk/pydantic/client.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/oauth/clients/{clientId}` `patch`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.other.get_ip_list`<a id="launchdarklyotherget_ip_list"></a>

Get a list of IP ranges the LaunchDarkly service uses. You can use this list to allow LaunchDarkly through your firewall. We post upcoming changes to this list in advance on our [status page](https://status.launchdarkly.com/). <br /><br />In the sandbox, click 'Try it' and enter any string in the 'Authorization' field to test this endpoint.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_ip_list_response = launchdarkly.other.get_ip_list()
```

#### 🔄 Return<a id="🔄-return"></a>

[`IpList`](./launch_darkly_python_sdk/pydantic/ip_list.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/public-ip-list` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.other.get_openapi_spec`<a id="launchdarklyotherget_openapi_spec"></a>

Get the latest version of the OpenAPI specification for LaunchDarkly's API in JSON format. In the sandbox, click 'Try it' and enter any string in the 'Authorization' field to test this endpoint.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
launchdarkly.other.get_openapi_spec()
```

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/openapi.json` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.other.get_resource_categories`<a id="launchdarklyotherget_resource_categories"></a>

Get all of the resource categories the API supports. In the sandbox, click 'Try it' and enter any string in the 'Authorization' field to test this endpoint.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_resource_categories_response = launchdarkly.other.get_resource_categories()
```

#### 🔄 Return<a id="🔄-return"></a>

[`RootResponse`](./launch_darkly_python_sdk/pydantic/root_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.other.get_version_information`<a id="launchdarklyotherget_version_information"></a>

Get the latest API version, the list of valid API versions in ascending order, and the version being used for this request. These are all in the external, date-based format.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_version_information_response = launchdarkly.other.get_version_information()
```

#### 🔄 Return<a id="🔄-return"></a>

[`VersionsRep`](./launch_darkly_python_sdk/pydantic/versions_rep.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/versions` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.projects.create_new_project`<a id="launchdarklyprojectscreate_new_project"></a>

Create a new project with the given key and name. Project keys must be unique within an account.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
create_new_project_response = launchdarkly.projects.create_new_project(
    name="My Project",
    key="project-key-123abc",
    tags=["ops"],
    include_in_snippet_by_default=True,
    default_client_side_availability={
        "using_environment_id": True,
        "using_mobile_key": True,
    },
    environments=[
        {
            "tags": ["ops"],
            "name": "My Environment",
            "key": "environment-key-123abc",
            "color": "F5A623",
            "default_ttl": 5,
            "secure_mode": True,
            "default_track_events": False,
            "confirm_changes": False,
            "require_comments": False,
            "critical": True,
        }
    ],
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### name: `str`<a id="name-str"></a>

A human-friendly name for the project.

##### key: `str`<a id="key-str"></a>

A unique key used to reference the project in your code.

##### tags: [`ProjectPostTags`](./launch_darkly_python_sdk/type/project_post_tags.py)<a id="tags-projectposttagslaunch_darkly_python_sdktypeproject_post_tagspy"></a>

##### include_in_snippet_by_default: `bool`<a id="include_in_snippet_by_default-bool"></a>

Whether or not flags created in this project are made available to the client-side JavaScript SDK by default.

##### default_client_side_availability: [`DefaultClientSideAvailabilityPost`](./launch_darkly_python_sdk/type/default_client_side_availability_post.py)<a id="default_client_side_availability-defaultclientsideavailabilitypostlaunch_darkly_python_sdktypedefault_client_side_availability_postpy"></a>


##### environments: List[`EnvironmentPost`]<a id="environments-listenvironmentpost"></a>

Creates the provided environments for this project. If omitted default environments will be created instead.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`ProjectPost`](./launch_darkly_python_sdk/type/project_post.py)
#### 🔄 Return<a id="🔄-return"></a>

[`ProjectRep`](./launch_darkly_python_sdk/pydantic/project_rep.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/projects` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.projects.delete_by_project_key`<a id="launchdarklyprojectsdelete_by_project_key"></a>

Delete a project by key. Use this endpoint with caution. Deleting a project will delete all associated environments and feature flags. You cannot delete the last project in an account.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
launchdarkly.projects.delete_by_project_key(
    project_key="projectKey_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/projects/{projectKey}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.projects.get_flag_defaults`<a id="launchdarklyprojectsget_flag_defaults"></a>

Get the flag defaults for a specific project.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_flag_defaults_response = launchdarkly.projects.get_flag_defaults(
    project_key="projectKey_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

#### 🔄 Return<a id="🔄-return"></a>

[`FlagDefaultsRep`](./launch_darkly_python_sdk/pydantic/flag_defaults_rep.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/projects/{projectKey}/flag-defaults` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.projects.list_projects_default`<a id="launchdarklyprojectslist_projects_default"></a>

Return a list of projects.

By default, this returns the first 20 projects. Page through this list with the `limit` parameter and by following the `first`, `prev`, `next`, and `last` links in the `_links` field that returns. If those links do not appear, the pages they refer to don't exist. For example, the `first` and `prev` links will be missing from the response on the first page, because there is no previous page and you cannot return to the first page when you are already on the first page.

### Filtering projects<a id="filtering-projects"></a>

LaunchDarkly supports two fields for filters:
- `query` is a string that matches against the projects' names and keys. It is not case sensitive.
- `tags` is a `+`-separated list of project tags. It filters the list of projects that have all of the tags in the list.

For example, the filter `filter=query:abc,tags:tag-1+tag-2` matches projects with the string `abc` in their name or key and also are tagged with `tag-1` and `tag-2`. The filter is not case-sensitive.

The documented values for `filter` query parameters are prior to URL encoding. For example, the `+` in `filter=tags:tag-1+tag-2` must be encoded to `%2B`.

### Sorting projects<a id="sorting-projects"></a>

LaunchDarkly supports two fields for sorting:
- `name` sorts by project name.
- `createdOn` sorts by the creation date of the project.

For example, `sort=name` sorts the response by project name in ascending order.

### Expanding the projects response<a id="expanding-the-projects-response"></a>

LaunchDarkly supports one field for expanding the "List projects" response. By default, these fields are **not** included in the response.

To expand the response, append the `expand` query parameter and add a comma-separated list with the `environments` field.

`Environments` includes a paginated list of the project environments.
* `environments` includes a paginated list of the project environments.

For example, `expand=environments` includes the `environments` field for each project in the response.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_projects_default_response = launchdarkly.projects.list_projects_default(
    limit=1,
    offset=1,
    filter="string_example",
    sort="string_example",
    expand="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### limit: `int`<a id="limit-int"></a>

The number of projects to return in the response. Defaults to 20.

##### offset: `int`<a id="offset-int"></a>

Where to start in the list. Use this with pagination. For example, an offset of 10 skips the first ten items and returns the next `limit` items.

##### filter: `str`<a id="filter-str"></a>

A comma-separated list of filters. Each filter is constructed as `field:value`.

##### sort: `str`<a id="sort-str"></a>

A comma-separated list of fields to sort by. Fields prefixed by a dash ( - ) sort in descending order.

##### expand: `str`<a id="expand-str"></a>

A comma-separated list of properties that can reveal additional information in the response.

#### 🔄 Return<a id="🔄-return"></a>

[`Projects`](./launch_darkly_python_sdk/pydantic/projects.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/projects` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.projects.single_by_project_key`<a id="launchdarklyprojectssingle_by_project_key"></a>

Get a single project by key.

### Expanding the project response<a id="expanding-the-project-response"></a>

LaunchDarkly supports one field for expanding the "Get project" response. By default, these fields are **not** included in the response.

To expand the response, append the `expand` query parameter and add a comma-separated list with any of the following fields:
* `environments` includes a paginated list of the project environments.

For example, `expand=environments` includes the `environments` field for the project in the response.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
single_by_project_key_response = launchdarkly.projects.single_by_project_key(
    project_key="projectKey_example",
    expand="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key.

##### expand: `str`<a id="expand-str"></a>

A comma-separated list of properties that can reveal additional information in the response.

#### 🔄 Return<a id="🔄-return"></a>

[`Project`](./launch_darkly_python_sdk/pydantic/project.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/projects/{projectKey}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.projects.update_flag_default`<a id="launchdarklyprojectsupdate_flag_default"></a>

Update a flag default. Updating a flag default uses a [JSON patch](https://datatracker.ietf.org/doc/html/rfc6902) or [JSON merge patch](https://datatracker.ietf.org/doc/html/rfc7386) representation of the desired changes. To learn more, read [Updates](https://apidocs.launchdarkly.com).

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
update_flag_default_response = launchdarkly.projects.update_flag_default(
    body=[
        {
            "op": "replace",
            "path": "/exampleField",
            "value": None,
        }
    ],
    project_key="projectKey_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### requestBody: [`JSONPatch`](./launch_darkly_python_sdk/type/json_patch.py)<a id="requestbody-jsonpatchlaunch_darkly_python_sdktypejson_patchpy"></a>

#### 🔄 Return<a id="🔄-return"></a>

[`UpsertPayloadRep`](./launch_darkly_python_sdk/pydantic/upsert_payload_rep.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/projects/{projectKey}/flag-defaults` `patch`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.projects.update_flag_defaults_for_project`<a id="launchdarklyprojectsupdate_flag_defaults_for_project"></a>

Create or update flag defaults for a project.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
update_flag_defaults_for_project_response = launchdarkly.projects.update_flag_defaults_for_project(
    tags=["tag-1", "tag-2"],
    temporary=True,
    boolean_defaults={
        "true_display_name": "True",
        "false_display_name": "False",
        "true_description": "serve true",
        "false_description": "serve false",
        "on_variation": 0,
        "off_variation": 1,
    },
    default_client_side_availability={
        "using_mobile_key": True,
        "using_environment_id": True,
    },
    project_key="projectKey_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### tags: [`UpsertFlagDefaultsPayloadTags`](./launch_darkly_python_sdk/type/upsert_flag_defaults_payload_tags.py)<a id="tags-upsertflagdefaultspayloadtagslaunch_darkly_python_sdktypeupsert_flag_defaults_payload_tagspy"></a>

##### temporary: `bool`<a id="temporary-bool"></a>

Whether the flag should be temporary by default

##### boolean_defaults: [`BooleanFlagDefaults`](./launch_darkly_python_sdk/type/boolean_flag_defaults.py)<a id="boolean_defaults-booleanflagdefaultslaunch_darkly_python_sdktypeboolean_flag_defaultspy"></a>


##### default_client_side_availability: [`DefaultClientSideAvailability`](./launch_darkly_python_sdk/type/default_client_side_availability.py)<a id="default_client_side_availability-defaultclientsideavailabilitylaunch_darkly_python_sdktypedefault_client_side_availabilitypy"></a>


##### project_key: `str`<a id="project_key-str"></a>

The project key

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`UpsertFlagDefaultsPayload`](./launch_darkly_python_sdk/type/upsert_flag_defaults_payload.py)
#### 🔄 Return<a id="🔄-return"></a>

[`UpsertPayloadRep`](./launch_darkly_python_sdk/pydantic/upsert_payload_rep.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/projects/{projectKey}/flag-defaults` `put`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.projects.update_project_patch`<a id="launchdarklyprojectsupdate_project_patch"></a>

Update a project. Updating a project uses a [JSON patch](https://datatracker.ietf.org/doc/html/rfc6902) representation of the desired changes. To learn more, read [Updates](https://apidocs.launchdarkly.com).<br/><br/>To add an element to the project fields that are arrays, set the `path` to the name of the field and then append `/<array index>`. Use `/0` to add to the beginning of the array. Use `/-` to add to the end of the array.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
update_project_patch_response = launchdarkly.projects.update_project_patch(
    body=[{"op":"add","path":"/tags/0","value":"another-tag"}],
    project_key="projectKey_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### requestBody: [`JSONPatch`](./launch_darkly_python_sdk/type/json_patch.py)<a id="requestbody-jsonpatchlaunch_darkly_python_sdktypejson_patchpy"></a>

#### 🔄 Return<a id="🔄-return"></a>

[`ProjectRep`](./launch_darkly_python_sdk/pydantic/project_rep.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/projects/{projectKey}` `patch`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.relay_proxy_configurations.create_new_config`<a id="launchdarklyrelay_proxy_configurationscreate_new_config"></a>

Create a Relay Proxy config.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
create_new_config_response = launchdarkly.relay_proxy_configurations.create_new_config(
    name="string_example",
    policy=[
        {
            "resources": ["proj/*:env/*;qa_*:/flag/*"],
            "actions": ["*"],
            "effect": "allow",
        }
    ],
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### name: `str`<a id="name-str"></a>

A human-friendly name for the Relay Proxy configuration

##### policy: List[`Statement`]<a id="policy-liststatement"></a>

A description of what environments and projects the Relay Proxy should include or exclude. To learn more, read [Writing an inline policy](https://docs.launchdarkly.com/home/relay-proxy/automatic-configuration#writing-an-inline-policy).

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`RelayAutoConfigPost`](./launch_darkly_python_sdk/type/relay_auto_config_post.py)
#### 🔄 Return<a id="🔄-return"></a>

[`RelayAutoConfigRep`](./launch_darkly_python_sdk/pydantic/relay_auto_config_rep.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/account/relay-auto-configs` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.relay_proxy_configurations.delete_by_id`<a id="launchdarklyrelay_proxy_configurationsdelete_by_id"></a>

Delete a Relay Proxy config.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
launchdarkly.relay_proxy_configurations.delete_by_id(
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

The relay auto config id

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/account/relay-auto-configs/{id}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.relay_proxy_configurations.get_single_by_id`<a id="launchdarklyrelay_proxy_configurationsget_single_by_id"></a>

Get a single Relay Proxy auto config by ID.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_single_by_id_response = launchdarkly.relay_proxy_configurations.get_single_by_id(
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

The relay auto config id

#### 🔄 Return<a id="🔄-return"></a>

[`RelayAutoConfigRep`](./launch_darkly_python_sdk/pydantic/relay_auto_config_rep.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/account/relay-auto-configs/{id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.relay_proxy_configurations.list`<a id="launchdarklyrelay_proxy_configurationslist"></a>

Get a list of Relay Proxy configurations in the account.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_response = launchdarkly.relay_proxy_configurations.list()
```

#### 🔄 Return<a id="🔄-return"></a>

[`RelayAutoConfigCollectionRep`](./launch_darkly_python_sdk/pydantic/relay_auto_config_collection_rep.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/account/relay-auto-configs` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.relay_proxy_configurations.reset_secret_key_with_expiry`<a id="launchdarklyrelay_proxy_configurationsreset_secret_key_with_expiry"></a>

Reset a Relay Proxy configuration's secret key with an optional expiry time for the old key.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
reset_secret_key_with_expiry_response = launchdarkly.relay_proxy_configurations.reset_secret_key_with_expiry(
    id="id_example",
    expiry=1,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

The Relay Proxy configuration ID

##### expiry: `int`<a id="expiry-int"></a>

An expiration time for the old Relay Proxy configuration key, expressed as a Unix epoch time in milliseconds. By default, the Relay Proxy configuration will expire immediately.

#### 🔄 Return<a id="🔄-return"></a>

[`RelayAutoConfigRep`](./launch_darkly_python_sdk/pydantic/relay_auto_config_rep.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/account/relay-auto-configs/{id}/reset` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.relay_proxy_configurations.update_config_patch`<a id="launchdarklyrelay_proxy_configurationsupdate_config_patch"></a>

Update a Relay Proxy configuration. Updating a configuration uses a [JSON patch](https://datatracker.ietf.org/doc/html/rfc6902) or [JSON merge patch](https://datatracker.ietf.org/doc/html/rfc7386) representation of the desired changes. To learn more, read [Updates](https://apidocs.launchdarkly.com).

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
update_config_patch_response = launchdarkly.relay_proxy_configurations.update_config_patch(
    patch=[
        {
            "op": "replace",
            "path": "/exampleField",
            "value": None,
        }
    ],
    id="id_example",
    comment="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### patch: [`JSONPatch`](./launch_darkly_python_sdk/type/json_patch.py)<a id="patch-jsonpatchlaunch_darkly_python_sdktypejson_patchpy"></a>

##### id: `str`<a id="id-str"></a>

The relay auto config id

##### comment: `str`<a id="comment-str"></a>

Optional comment

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`PatchWithComment`](./launch_darkly_python_sdk/type/patch_with_comment.py)
#### 🔄 Return<a id="🔄-return"></a>

[`RelayAutoConfigRep`](./launch_darkly_python_sdk/pydantic/relay_auto_config_rep.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/account/relay-auto-configs/{id}` `patch`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.release_pipelines_(beta).create_new_pipeline`<a id="launchdarklyrelease_pipelines_betacreate_new_pipeline"></a>

Creates a new release pipeline.

The first release pipeline you create is automatically set as the default release pipeline for your project. To change the default release pipeline, use the [Update project](https://apidocs.launchdarkly.com) API to set the `defaultReleasePipelineKey`.

You can create up to 20 release pipelines per project.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
create_new_pipeline_response = launchdarkly.release_pipelines_(beta).create_new_pipeline(
    key="standard-pipeline",
    name="Standard Pipeline",
    phases=[
        {
            "audiences": [
                {
                    "environment_key": "environment_key_example",
                    "name": "name_example",
                }
            ],
            "name": "Phase 1 - Testing",
        }
    ],
    project_key="projectKey_example",
    tags=["example-tag"],
    description="Standard pipeline to roll out to production",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### key: `str`<a id="key-str"></a>

The unique identifier of this release pipeline

##### name: `str`<a id="name-str"></a>

The name of the release pipeline

##### phases: List[`CreatePhaseInput`]<a id="phases-listcreatephaseinput"></a>

A logical grouping of one or more environments that share attributes for rolling out changes

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### tags: [`CreateReleasePipelineInputTags`](./launch_darkly_python_sdk/type/create_release_pipeline_input_tags.py)<a id="tags-createreleasepipelineinputtagslaunch_darkly_python_sdktypecreate_release_pipeline_input_tagspy"></a>

##### description: `str`<a id="description-str"></a>

The release pipeline description

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`CreateReleasePipelineInput`](./launch_darkly_python_sdk/type/create_release_pipeline_input.py)
#### 🔄 Return<a id="🔄-return"></a>

[`ReleasePipeline`](./launch_darkly_python_sdk/pydantic/release_pipeline.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/projects/{projectKey}/release-pipelines` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.release_pipelines_(beta).delete_pipeline`<a id="launchdarklyrelease_pipelines_betadelete_pipeline"></a>

Deletes a release pipeline.

You cannot delete the default release pipeline.

If you want to delete a release pipeline that is currently the default, create a second release pipeline and set it as the default. Then delete the first release pipeline. To change the default release pipeline, use the [Update project](https://apidocs.launchdarkly.com) API to set the `defaultReleasePipelineKey`.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
launchdarkly.release_pipelines_(beta).delete_pipeline(
    project_key="projectKey_example",
    pipeline_key="pipelineKey_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### pipeline_key: `str`<a id="pipeline_key-str"></a>

The release pipeline key

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/projects/{projectKey}/release-pipelines/{pipelineKey}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.release_pipelines_(beta).get_all_release_pipelines`<a id="launchdarklyrelease_pipelines_betaget_all_release_pipelines"></a>

Get all release pipelines for a project.

### Filtering release pipelines<a id="filtering-release-pipelines"></a>

LaunchDarkly supports the following fields for filters:

- `query` is a string that matches against the release pipeline `key`, `name`, and `description`. It is not case sensitive. For example: `?filter=query:examplePipeline`.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_all_release_pipelines_response = launchdarkly.release_pipelines_(beta).get_all_release_pipelines(
    project_key="projectKey_example",
    filter="string_example",
    limit=1,
    offset=1,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### filter: `str`<a id="filter-str"></a>

A comma-separated list of filters. Each filter is of the form field:value. Read the endpoint description for a full list of available filter fields.

##### limit: `int`<a id="limit-int"></a>

The maximum number of items to return. Defaults to 20.

##### offset: `int`<a id="offset-int"></a>

Where to start in the list. Defaults to 0. Use this with pagination. For example, an offset of 10 skips the first ten items and then returns the next items in the list, up to the query `limit`.

#### 🔄 Return<a id="🔄-return"></a>

[`ReleasePipelineCollection`](./launch_darkly_python_sdk/pydantic/release_pipeline_collection.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/projects/{projectKey}/release-pipelines` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.release_pipelines_(beta).get_by_pipe_key`<a id="launchdarklyrelease_pipelines_betaget_by_pipe_key"></a>

Get a release pipeline by key

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_by_pipe_key_response = launchdarkly.release_pipelines_(beta).get_by_pipe_key(
    project_key="projectKey_example",
    pipeline_key="pipelineKey_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### pipeline_key: `str`<a id="pipeline_key-str"></a>

The release pipeline key

#### 🔄 Return<a id="🔄-return"></a>

[`ReleasePipeline`](./launch_darkly_python_sdk/pydantic/release_pipeline.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/projects/{projectKey}/release-pipelines/{pipelineKey}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.release_pipelines_(beta).update_pipeline_patch`<a id="launchdarklyrelease_pipelines_betaupdate_pipeline_patch"></a>

Updates a release pipeline. Updating a release pipeline uses a [JSON patch](https://datatracker.ietf.org/doc/html/rfc6902) representation of the desired changes. To learn more, read [Updates](https://apidocs.launchdarkly.com).

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
update_pipeline_patch_response = launchdarkly.release_pipelines_(beta).update_pipeline_patch(
    project_key="projectKey_example",
    pipeline_key="pipelineKey_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### pipeline_key: `str`<a id="pipeline_key-str"></a>

The release pipeline key

#### 🔄 Return<a id="🔄-return"></a>

[`ReleasePipeline`](./launch_darkly_python_sdk/pydantic/release_pipeline.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/projects/{projectKey}/release-pipelines/{pipelineKey}` `patch`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.releases_(beta).get_current_release`<a id="launchdarklyreleases_betaget_current_release"></a>

Get currently active release for a flag

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_current_release_response = launchdarkly.releases_(beta).get_current_release(
    project_key="projectKey_example",
    flag_key="flagKey_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### flag_key: `str`<a id="flag_key-str"></a>

The flag key

#### 🔄 Return<a id="🔄-return"></a>

[`Release`](./launch_darkly_python_sdk/pydantic/release.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/flags/{projectKey}/{flagKey}/release` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.releases_(beta).update_active_release_patch`<a id="launchdarklyreleases_betaupdate_active_release_patch"></a>

Update currently active release for a flag. Updating releases requires the [JSON patch](https://datatracker.ietf.org/doc/html/rfc6902) format. To learn more, read [Updates](https://apidocs.launchdarkly.com).

You can only use this endpoint to mark a release phase complete or incomplete. To indicate which phase to update, use the array index in the `path`. For example, to mark the first phase of a release as complete, use the following request body:

```
  [
    {
      "op": "replace",
      "path": "/phase/0/complete",
      "value": true
    }
  ]
```


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
update_active_release_patch_response = launchdarkly.releases_(beta).update_active_release_patch(
    body=[{"op":"replace","path":"/phases/0/complete","value":true}],
    project_key="projectKey_example",
    flag_key="flagKey_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### flag_key: `str`<a id="flag_key-str"></a>

The flag key

##### requestBody: [`JSONPatch`](./launch_darkly_python_sdk/type/json_patch.py)<a id="requestbody-jsonpatchlaunch_darkly_python_sdktypejson_patchpy"></a>

#### 🔄 Return<a id="🔄-return"></a>

[`Release`](./launch_darkly_python_sdk/pydantic/release.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/flags/{projectKey}/{flagKey}/release` `patch`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.scheduled_changes.create_workflow`<a id="launchdarklyscheduled_changescreate_workflow"></a>

Create scheduled changes for a feature flag. If the `ignoreConficts` query parameter is false and there are conflicts between these instructions and existing scheduled changes, the request will fail. If the parameter is true and there are conflicts, the request will succeed.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
create_workflow_response = launchdarkly.scheduled_changes.create_workflow(
    execution_date=1,
    instructions=[
        {
            "key": None,
        }
    ],
    project_key="projectKey_example",
    feature_flag_key="featureFlagKey_example",
    environment_key="environmentKey_example",
    comment="optional comment",
    ignore_conflicts=True,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### execution_date: `int`<a id="execution_date-int"></a>

##### instructions: [`Instructions`](./launch_darkly_python_sdk/type/instructions.py)<a id="instructions-instructionslaunch_darkly_python_sdktypeinstructionspy"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### feature_flag_key: `str`<a id="feature_flag_key-str"></a>

The feature flag key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

##### comment: `str`<a id="comment-str"></a>

Optional comment describing the scheduled changes

##### ignore_conflicts: `bool`<a id="ignore_conflicts-bool"></a>

Whether to succeed (`true`) or fail (`false`) when these instructions conflict with existing scheduled changes

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`PostFlagScheduledChangesInput`](./launch_darkly_python_sdk/type/post_flag_scheduled_changes_input.py)
#### 🔄 Return<a id="🔄-return"></a>

[`FeatureFlagScheduledChange`](./launch_darkly_python_sdk/pydantic/feature_flag_scheduled_change.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/projects/{projectKey}/flags/{featureFlagKey}/environments/{environmentKey}/scheduled-changes` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.scheduled_changes.delete_workflow`<a id="launchdarklyscheduled_changesdelete_workflow"></a>

Delete a scheduled changes workflow.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
launchdarkly.scheduled_changes.delete_workflow(
    project_key="projectKey_example",
    feature_flag_key="featureFlagKey_example",
    environment_key="environmentKey_example",
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### feature_flag_key: `str`<a id="feature_flag_key-str"></a>

The feature flag key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

##### id: `str`<a id="id-str"></a>

The scheduled change id

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/projects/{projectKey}/flags/{featureFlagKey}/environments/{environmentKey}/scheduled-changes/{id}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.scheduled_changes.get_by_id`<a id="launchdarklyscheduled_changesget_by_id"></a>

Get a scheduled change that will be applied to the feature flag by ID.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_by_id_response = launchdarkly.scheduled_changes.get_by_id(
    project_key="projectKey_example",
    feature_flag_key="featureFlagKey_example",
    environment_key="environmentKey_example",
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### feature_flag_key: `str`<a id="feature_flag_key-str"></a>

The feature flag key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

##### id: `str`<a id="id-str"></a>

The scheduled change id

#### 🔄 Return<a id="🔄-return"></a>

[`FeatureFlagScheduledChange`](./launch_darkly_python_sdk/pydantic/feature_flag_scheduled_change.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/projects/{projectKey}/flags/{featureFlagKey}/environments/{environmentKey}/scheduled-changes/{id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.scheduled_changes.list_changes`<a id="launchdarklyscheduled_changeslist_changes"></a>

Get a list of scheduled changes that will be applied to the feature flag.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_changes_response = launchdarkly.scheduled_changes.list_changes(
    project_key="projectKey_example",
    feature_flag_key="featureFlagKey_example",
    environment_key="environmentKey_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### feature_flag_key: `str`<a id="feature_flag_key-str"></a>

The feature flag key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

#### 🔄 Return<a id="🔄-return"></a>

[`FeatureFlagScheduledChanges`](./launch_darkly_python_sdk/pydantic/feature_flag_scheduled_changes.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/projects/{projectKey}/flags/{featureFlagKey}/environments/{environmentKey}/scheduled-changes` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.scheduled_changes.update_workflow`<a id="launchdarklyscheduled_changesupdate_workflow"></a>


Update a scheduled change, overriding existing instructions with the new ones. Updating a scheduled change uses the semantic patch format.

To make a semantic patch request, you must append `domain-model=launchdarkly.semanticpatch` to your `Content-Type` header. To learn more, read [Updates using semantic patch](https://apidocs.launchdarkly.com).

### Instructions<a id="instructions"></a>

Semantic patch requests support the following `kind` instructions for updating scheduled changes.

<details>
<summary>Click to expand instructions for <strong>updating scheduled changes</strong></summary>

#### deleteScheduledChange<a id="deletescheduledchange"></a>

Removes the scheduled change.

Here's an example:

```json
{
  "instructions": [{ "kind": "deleteScheduledChange" }]
}
```

#### replaceScheduledChangesInstructions<a id="replacescheduledchangesinstructions"></a>

Removes the existing scheduled changes and replaces them with the new instructions.

##### Parameters<a id="parameters"></a>

- `value`: An array of the new actions to perform when the execution date for these scheduled changes arrives. Supported scheduled actions are `turnFlagOn` and `turnFlagOff`.

Here's an example that replaces the scheduled changes with new instructions to turn flag targeting off:

```json
{
  "instructions": [
    {
      "kind": "replaceScheduledChangesInstructions",
      "value": [ {"kind": "turnFlagOff"} ]
    }
  ]
}
```

#### updateScheduledChangesExecutionDate<a id="updatescheduledchangesexecutiondate"></a>

Updates the execution date for the scheduled changes.

##### Parameters<a id="parameters"></a>

- `value`: the new execution date, in Unix milliseconds.

Here's an example:

```json
{
  "instructions": [
    {
      "kind": "updateScheduledChangesExecutionDate",
      "value": 1754092860000
    }
  ]
}
```

</details>


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
update_workflow_response = launchdarkly.scheduled_changes.update_workflow(
    instructions=[
        {
            "key": None,
        }
    ],
    project_key="projectKey_example",
    feature_flag_key="featureFlagKey_example",
    environment_key="environmentKey_example",
    id="id_example",
    comment="optional comment",
    ignore_conflicts=True,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### instructions: [`Instructions`](./launch_darkly_python_sdk/type/instructions.py)<a id="instructions-instructionslaunch_darkly_python_sdktypeinstructionspy"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### feature_flag_key: `str`<a id="feature_flag_key-str"></a>

The feature flag key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

##### id: `str`<a id="id-str"></a>

The scheduled change ID

##### comment: `str`<a id="comment-str"></a>

Optional comment describing the update to the scheduled changes

##### ignore_conflicts: `bool`<a id="ignore_conflicts-bool"></a>

Whether to succeed (`true`) or fail (`false`) when these new instructions conflict with existing scheduled changes

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`FlagScheduledChangesInput`](./launch_darkly_python_sdk/type/flag_scheduled_changes_input.py)
#### 🔄 Return<a id="🔄-return"></a>

[`FeatureFlagScheduledChange`](./launch_darkly_python_sdk/pydantic/feature_flag_scheduled_change.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/projects/{projectKey}/flags/{featureFlagKey}/environments/{environmentKey}/scheduled-changes/{id}` `patch`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.segments.create_segment`<a id="launchdarklysegmentscreate_segment"></a>

Create a new segment.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
create_segment_response = launchdarkly.segments.create_segment(
    name="Example segment",
    key="segment-key-123abc",
    project_key="projectKey_example",
    environment_key="environmentKey_example",
    tags=["testing"],
    description="Bundle our sample customers together",
    unbounded=False,
    unbounded_context_kind="device",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### name: `str`<a id="name-str"></a>

A human-friendly name for the segment

##### key: `str`<a id="key-str"></a>

A unique key used to reference the segment

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

##### tags: [`SegmentBodyTags`](./launch_darkly_python_sdk/type/segment_body_tags.py)<a id="tags-segmentbodytagslaunch_darkly_python_sdktypesegment_body_tagspy"></a>

##### description: `str`<a id="description-str"></a>

A description of the segment's purpose

##### unbounded: `bool`<a id="unbounded-bool"></a>

Whether to create a standard segment (<code>false</code>) or a big segment (<code>true</code>). Standard segments include rule-based and smaller list-based segments. Big segments include larger list-based segments and synced segments. Only use a big segment if you need to add more than 15,000 individual targets.

##### unbounded_context_kind: `str`<a id="unbounded_context_kind-str"></a>

For big segments, the targeted context kind.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`SegmentBody`](./launch_darkly_python_sdk/type/segment_body.py)
#### 🔄 Return<a id="🔄-return"></a>

[`UserSegment`](./launch_darkly_python_sdk/pydantic/user_segment.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/segments/{projectKey}/{environmentKey}` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.segments.evaluate_segment_memberships`<a id="launchdarklysegmentsevaluate_segment_memberships"></a>

For a given context instance with attributes, get membership details for all segments. In the request body, pass in the context instance.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
evaluate_segment_memberships_response = launchdarkly.segments.evaluate_segment_memberships(
    project_key="projectKey_example",
    environment_key="environmentKey_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`ContextInstance`](./launch_darkly_python_sdk/type/context_instance.py)
#### 🔄 Return<a id="🔄-return"></a>

[`ContextInstanceSegmentMemberships`](./launch_darkly_python_sdk/pydantic/context_instance_segment_memberships.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/projects/{projectKey}/environments/{environmentKey}/segments/evaluate` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.segments.get_context_membership`<a id="launchdarklysegmentsget_context_membership"></a>

Get the membership status (included/excluded) for a given context in this big segment. Big segments include larger list-based segments and synced segments. This operation does not support standard segments.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_context_membership_response = launchdarkly.segments.get_context_membership(
    project_key="projectKey_example",
    environment_key="environmentKey_example",
    segment_key="segmentKey_example",
    context_key="contextKey_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

##### segment_key: `str`<a id="segment_key-str"></a>

The segment key

##### context_key: `str`<a id="context_key-str"></a>

The context key

#### 🔄 Return<a id="🔄-return"></a>

[`BigSegmentTarget`](./launch_darkly_python_sdk/pydantic/big_segment_target.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/segments/{projectKey}/{environmentKey}/{segmentKey}/contexts/{contextKey}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.segments.get_expiring_targets`<a id="launchdarklysegmentsget_expiring_targets"></a>

Get a list of a segment's context targets that are scheduled for removal.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_expiring_targets_response = launchdarkly.segments.get_expiring_targets(
    project_key="projectKey_example",
    environment_key="environmentKey_example",
    segment_key="segmentKey_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

##### segment_key: `str`<a id="segment_key-str"></a>

The segment key

#### 🔄 Return<a id="🔄-return"></a>

[`ExpiringTargetGetResponse`](./launch_darkly_python_sdk/pydantic/expiring_target_get_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/segments/{projectKey}/{segmentKey}/expiring-targets/{environmentKey}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.segments.get_expiring_user_targets`<a id="launchdarklysegmentsget_expiring_user_targets"></a>

> ### Contexts are now available
>
> After you have upgraded your LaunchDarkly SDK to use contexts instead of users, you should use [Get expiring targets for segment](https://apidocs.launchdarkly.com) instead of this endpoint. To learn more, read [Contexts](https://docs.launchdarkly.com/home/contexts).

Get a list of a segment's user targets that are scheduled for removal.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_expiring_user_targets_response = launchdarkly.segments.get_expiring_user_targets(
    project_key="projectKey_example",
    environment_key="environmentKey_example",
    segment_key="segmentKey_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

##### segment_key: `str`<a id="segment_key-str"></a>

The segment key

#### 🔄 Return<a id="🔄-return"></a>

[`ExpiringUserTargetGetResponse`](./launch_darkly_python_sdk/pydantic/expiring_user_target_get_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/segments/{projectKey}/{segmentKey}/expiring-user-targets/{environmentKey}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.segments.get_segment_list`<a id="launchdarklysegmentsget_segment_list"></a>

Get a list of all segments in the given project.<br/><br/>Segments can be rule-based, list-based, or synced. Big segments include larger list-based segments and synced segments. Some fields in the response only apply to big segments.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_segment_list_response = launchdarkly.segments.get_segment_list(
    project_key="projectKey_example",
    environment_key="environmentKey_example",
    limit=1,
    offset=1,
    sort="string_example",
    filter="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

##### limit: `int`<a id="limit-int"></a>

The number of segments to return. Defaults to 50.

##### offset: `int`<a id="offset-int"></a>

Where to start in the list. Use this with pagination. For example, an offset of 10 skips the first ten items and then returns the next items in the list, up to the query `limit`.

##### sort: `str`<a id="sort-str"></a>

Accepts sorting order and fields. Fields can be comma separated. Possible fields are 'creationDate', 'name', 'lastModified'. Example: `sort=name` sort by names ascending or `sort=-name,creationDate` sort by names descending and creationDate ascending.

##### filter: `str`<a id="filter-str"></a>

Accepts filter by kind, query, tags, unbounded, or external. To filter by kind or query, use the `equals` operator. To filter by tags, use the `anyOf` operator. Query is a 'fuzzy' search across segment key, name, and description. Example: `filter=tags anyOf ['enterprise', 'beta'],query equals 'toggle'` returns segments with 'toggle' in their key, name, or description that also have 'enterprise' or 'beta' as a tag. To filter by unbounded, use the `equals` operator. Example: `filter=unbounded equals true`. To filter by external, use the `exists` operator. Example: `filter=external exists true`.

#### 🔄 Return<a id="🔄-return"></a>

[`UserSegments`](./launch_darkly_python_sdk/pydantic/user_segments.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/segments/{projectKey}/{environmentKey}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.segments.get_user_membership_status`<a id="launchdarklysegmentsget_user_membership_status"></a>

> ### Contexts are now available
>
> After you have upgraded your LaunchDarkly SDK to use contexts instead of users, you should use [Get expiring targets for segment](https://apidocs.launchdarkly.com) instead of this endpoint. To learn more, read [Contexts](https://docs.launchdarkly.com/home/contexts).

Get the membership status (included/excluded) for a given user in this big segment. This operation does not support standard segments.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_user_membership_status_response = launchdarkly.segments.get_user_membership_status(
    project_key="projectKey_example",
    environment_key="environmentKey_example",
    segment_key="segmentKey_example",
    user_key="userKey_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

##### segment_key: `str`<a id="segment_key-str"></a>

The segment key

##### user_key: `str`<a id="user_key-str"></a>

The user key

#### 🔄 Return<a id="🔄-return"></a>

[`BigSegmentTarget`](./launch_darkly_python_sdk/pydantic/big_segment_target.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/segments/{projectKey}/{environmentKey}/{segmentKey}/users/{userKey}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.segments.remove_segment`<a id="launchdarklysegmentsremove_segment"></a>

Delete a segment.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
launchdarkly.segments.remove_segment(
    project_key="projectKey_example",
    environment_key="environmentKey_example",
    segment_key="segmentKey_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

##### segment_key: `str`<a id="segment_key-str"></a>

The segment key

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/segments/{projectKey}/{environmentKey}/{segmentKey}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.segments.single_segment_by_key`<a id="launchdarklysegmentssingle_segment_by_key"></a>

Get a single segment by key.<br/><br/>Segments can be rule-based, list-based, or synced. Big segments include larger list-based segments and synced segments. Some fields in the response only apply to big segments.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
single_segment_by_key_response = launchdarkly.segments.single_segment_by_key(
    project_key="projectKey_example",
    environment_key="environmentKey_example",
    segment_key="segmentKey_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

##### segment_key: `str`<a id="segment_key-str"></a>

The segment key

#### 🔄 Return<a id="🔄-return"></a>

[`UserSegment`](./launch_darkly_python_sdk/pydantic/user_segment.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/segments/{projectKey}/{environmentKey}/{segmentKey}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.segments.update_context_targets`<a id="launchdarklysegmentsupdate_context_targets"></a>

Update context targets included or excluded in a big segment. Big segments include larger list-based segments and synced segments. This operation does not support standard segments.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
launchdarkly.segments.update_context_targets(
    project_key="projectKey_example",
    environment_key="environmentKey_example",
    segment_key="segmentKey_example",
    included={
    },
    excluded={
    },
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

##### segment_key: `str`<a id="segment_key-str"></a>

The segment key

##### included: [`SegmentUserList`](./launch_darkly_python_sdk/type/segment_user_list.py)<a id="included-segmentuserlistlaunch_darkly_python_sdktypesegment_user_listpy"></a>


##### excluded: [`SegmentUserList`](./launch_darkly_python_sdk/type/segment_user_list.py)<a id="excluded-segmentuserlistlaunch_darkly_python_sdktypesegment_user_listpy"></a>


#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`SegmentUserState`](./launch_darkly_python_sdk/type/segment_user_state.py)
#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/segments/{projectKey}/{environmentKey}/{segmentKey}/contexts` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.segments.update_expiring_targets_for_segment`<a id="launchdarklysegmentsupdate_expiring_targets_for_segment"></a>


Update expiring context targets for a segment. Updating a context target expiration uses the semantic patch format.

To make a semantic patch request, you must append `domain-model=launchdarkly.semanticpatch` to your `Content-Type` header. To learn more, read [Updates using semantic patch](https://apidocs.launchdarkly.com).

If the request is well-formed but any of its instructions failed to process, this operation returns status code `200`. In this case, the response `errors` array will be non-empty.

### Instructions<a id="instructions"></a>

Semantic patch requests support the following `kind` instructions for updating expiring context targets.

<details>
<summary>Click to expand instructions for <strong>updating expiring context targets</strong></summary>

#### addExpiringTarget<a id="addexpiringtarget"></a>

Schedules a date and time when LaunchDarkly will remove a context from segment targeting. The segment must already have the context as an individual target.

##### Parameters<a id="parameters"></a>

- `targetType`: The type of individual target for this context. Must be either `included` or `excluded`.
- `contextKey`: The context key.
- `contextKind`: The kind of context being targeted.
- `value`: The date when the context should expire from the segment targeting, in Unix milliseconds.

Here's an example:

```json
{
  "instructions": [{
    "kind": "addExpiringTarget",
    "targetType": "included",
    "contextKey": "user-key-123abc",
    "contextKind": "user",
    "value": 1754092860000
  }]
}
```

#### updateExpiringTarget<a id="updateexpiringtarget"></a>

Updates the date and time when LaunchDarkly will remove a context from segment targeting.

##### Parameters<a id="parameters"></a>

- `targetType`: The type of individual target for this context. Must be either `included` or `excluded`.
- `contextKey`: The context key.
- `contextKind`: The kind of context being targeted.
- `value`: The new date when the context should expire from the segment targeting, in Unix milliseconds.
- `version`: (Optional) The version of the expiring target to update. If included, update will fail if version doesn't match current version of the expiring target.

Here's an example:

```json
{
  "instructions": [{
    "kind": "updateExpiringTarget",
    "targetType": "included",
    "contextKey": "user-key-123abc",
    "contextKind": "user",
    "value": 1754179260000
  }]
}
```

#### removeExpiringTarget<a id="removeexpiringtarget"></a>

Removes the scheduled expiration for the context in the segment.

##### Parameters<a id="parameters"></a>

- `targetType`: The type of individual target for this context. Must be either `included` or `excluded`.
- `contextKey`: The context key.
- `contextKind`: The kind of context being targeted.

Here's an example:

```json
{
  "instructions": [{
    "kind": "removeExpiringTarget",
    "targetType": "included",
    "contextKey": "user-key-123abc",
    "contextKind": "user",
  }]
}
```

</details>


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
update_expiring_targets_for_segment_response = launchdarkly.segments.update_expiring_targets_for_segment(
    instructions=[{
    "version": 1,
    "kind": "addExpiringTarget",
    "context_key": "context_key_example",
    "context_kind": "user",
    "target_type": "included",
    "value": 1653469200000,
}],
    project_key="projectKey_example",
    environment_key="environmentKey_example",
    segment_key="segmentKey_example",
    comment="optional comment",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### instructions: List[`PatchSegmentExpiringTargetInstruction`]<a id="instructions-listpatchsegmentexpiringtargetinstruction"></a>

Semantic patch instructions for the desired changes to the resource

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

##### segment_key: `str`<a id="segment_key-str"></a>

The segment key

##### comment: `str`<a id="comment-str"></a>

Optional description of changes

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`PatchSegmentExpiringTargetInputRep`](./launch_darkly_python_sdk/type/patch_segment_expiring_target_input_rep.py)
#### 🔄 Return<a id="🔄-return"></a>

[`ExpiringTargetPatchResponse`](./launch_darkly_python_sdk/pydantic/expiring_target_patch_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/segments/{projectKey}/{segmentKey}/expiring-targets/{environmentKey}` `patch`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.segments.update_expiring_targets_for_segment_0`<a id="launchdarklysegmentsupdate_expiring_targets_for_segment_0"></a>


> ### Contexts are now available
>
> After you have upgraded your LaunchDarkly SDK to use contexts instead of users, you should use [Update expiring targets for segment](https://apidocs.launchdarkly.com) instead of this endpoint. To learn more, read [Contexts](https://docs.launchdarkly.com/home/contexts).

Update expiring user targets for a segment. Updating a user target expiration uses the semantic patch format.

To make a semantic patch request, you must append `domain-model=launchdarkly.semanticpatch` to your `Content-Type` header. To learn more, read [Updates using semantic patch](https://apidocs.launchdarkly.com).

If the request is well-formed but any of its instructions failed to process, this operation returns status code `200`. In this case, the response `errors` array will be non-empty.

### Instructions<a id="instructions"></a>

Semantic patch requests support the following `kind` instructions for updating expiring user targets.

<details>
<summary>Click to expand instructions for <strong>updating expiring user targets</strong></summary>

#### addExpireUserTargetDate<a id="addexpireusertargetdate"></a>

Schedules a date and time when LaunchDarkly will remove a user from segment targeting.

##### Parameters<a id="parameters"></a>

- `targetType`: A segment's target type, must be either `included` or `excluded`.
- `userKey`: The user key.
- `value`: The date when the user should expire from the segment targeting, in Unix milliseconds.

#### updateExpireUserTargetDate<a id="updateexpireusertargetdate"></a>

Updates the date and time when LaunchDarkly will remove a user from segment targeting.

##### Parameters<a id="parameters"></a>

- `targetType`: A segment's target type, must be either `included` or `excluded`.
- `userKey`: The user key.
- `value`: The new date when the user should expire from the segment targeting, in Unix milliseconds.
- `version`: The segment version.

#### removeExpireUserTargetDate<a id="removeexpireusertargetdate"></a>

Removes the scheduled expiration for the user in the segment.

##### Parameters<a id="parameters"></a>

- `targetType`: A segment's target type, must be either `included` or `excluded`.
- `userKey`: The user key.

</details>


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
update_expiring_targets_for_segment_0_response = launchdarkly.segments.update_expiring_targets_for_segment_0(
    instructions=[{
    "version": 1,
    "kind": "addExpireUserTargetDate",
    "user_key": "user_key_example",
    "target_type": "included",
    "value": 1653469200000,
}],
    project_key="projectKey_example",
    environment_key="environmentKey_example",
    segment_key="segmentKey_example",
    comment="optional comment",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### instructions: List[`PatchSegmentInstruction`]<a id="instructions-listpatchsegmentinstruction"></a>

Semantic patch instructions for the desired changes to the resource

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

##### segment_key: `str`<a id="segment_key-str"></a>

The segment key

##### comment: `str`<a id="comment-str"></a>

Optional description of changes

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`PatchSegmentRequest`](./launch_darkly_python_sdk/type/patch_segment_request.py)
#### 🔄 Return<a id="🔄-return"></a>

[`ExpiringUserTargetPatchResponse`](./launch_darkly_python_sdk/pydantic/expiring_user_target_patch_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/segments/{projectKey}/{segmentKey}/expiring-user-targets/{environmentKey}` `patch`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.segments.update_semantic_patch`<a id="launchdarklysegmentsupdate_semantic_patch"></a>

Update a segment. The request body must be a valid semantic patch, JSON patch, or JSON merge patch. To learn more the different formats, read [Updates](https://apidocs.launchdarkly.com).

### Using semantic patches on a segment<a id="using-semantic-patches-on-a-segment"></a>

To make a semantic patch request, you must append `domain-model=launchdarkly.semanticpatch` to your `Content-Type` header. To learn more, read [Updates using semantic patch](https://apidocs.launchdarkly.com).

The body of a semantic patch request for updating segments requires an `environmentKey` in addition to `instructions` and an optional `comment`. The body of the request takes the following properties:

* `comment` (string): (Optional) A description of the update.
* `environmentKey` (string): (Required) The key of the LaunchDarkly environment.
* `instructions` (array): (Required) A list of actions the update should perform. Each action in the list must be an object with a `kind` property that indicates the instruction. If the action requires parameters, you must include those parameters as additional fields in the object.

### Instructions<a id="instructions"></a>

Semantic patch requests support the following `kind` instructions for updating segments.

<details>
<summary>Click to expand instructions for <strong>updating segments</strong></summary>

#### addIncludedTargets<a id="addincludedtargets"></a>

Adds context keys to the individual context targets included in the segment for the specified `contextKind`. Returns an error if this causes the same context key to be both included and excluded.

##### Parameters<a id="parameters"></a>

- `contextKind`: The context kind the targets should be added to.
- `values`: List of keys.

Here's an example:

```json
{
  "instructions": [{
    "kind": "addIncludedTargets",
    "contextKind": "org",
    "values": [ "org-key-123abc", "org-key-456def" ]
  }]
}
```

#### addIncludedUsers<a id="addincludedusers"></a>

Adds user keys to the individual user targets included in the segment. Returns an error if this causes the same user key to be both included and excluded. If you are working with contexts, use `addIncludedTargets` instead of this instruction.

##### Parameters<a id="parameters"></a>

- `values`: List of user keys.

Here's an example:

```json
{
  "instructions": [{
    "kind": "addIncludedUsers",
    "values": [ "user-key-123abc", "user-key-456def" ]
  }]
}
```

#### addExcludedTargets<a id="addexcludedtargets"></a>

Adds context keys to the individual context targets excluded in the segment for the specified `contextKind`. Returns an error if this causes the same context key to be both included and excluded.

##### Parameters<a id="parameters"></a>

- `contextKind`: The context kind the targets should be added to.
- `values`: List of keys.

Here's an example:

```json
{
  "instructions": [{
    "kind": "addExcludedTargets",
    "contextKind": "org",
    "values": [ "org-key-123abc", "org-key-456def" ]
  }]
}
```

#### addExcludedUsers<a id="addexcludedusers"></a>

Adds user keys to the individual user targets excluded from the segment. Returns an error if this causes the same user key to be both included and excluded. If you are working with contexts, use `addExcludedTargets` instead of this instruction.

##### Parameters<a id="parameters"></a>

- `values`: List of user keys.

Here's an example:

```json
{
  "instructions": [{
    "kind": "addExcludedUsers",
    "values": [ "user-key-123abc", "user-key-456def" ]
  }]
}
```

#### removeIncludedTargets<a id="removeincludedtargets"></a>

Removes context keys from the individual context targets included in the segment for the specified `contextKind`.

##### Parameters<a id="parameters"></a>

- `contextKind`: The context kind the targets should be removed from.
- `values`: List of keys.

Here's an example:

```json
{
  "instructions": [{
    "kind": "removeIncludedTargets",
    "contextKind": "org",
    "values": [ "org-key-123abc", "org-key-456def" ]
  }]
}
```

#### removeIncludedUsers<a id="removeincludedusers"></a>

Removes user keys from the individual user targets included in the segment. If you are working with contexts, use `removeIncludedTargets` instead of this instruction.

##### Parameters<a id="parameters"></a>

- `values`: List of user keys.

Here's an example:

```json
{
  "instructions": [{
    "kind": "removeIncludedUsers",
    "values": [ "user-key-123abc", "user-key-456def" ]
  }]
}
```

#### removeExcludedTargets<a id="removeexcludedtargets"></a>

Removes context keys from the individual context targets excluded from the segment for the specified `contextKind`.

##### Parameters<a id="parameters"></a>

- `contextKind`: The context kind the targets should be removed from.
- `values`: List of keys.

Here's an example:

```json
{
  "instructions": [{
    "kind": "removeExcludedTargets",
    "contextKind": "org",
    "values": [ "org-key-123abc", "org-key-456def" ]
  }]
}
```

#### removeExcludedUsers<a id="removeexcludedusers"></a>

Removes user keys from the individual user targets excluded from the segment. If you are working with contexts, use `removeExcludedTargets` instead of this instruction.

##### Parameters<a id="parameters"></a>

- `values`: List of user keys.

Here's an example:

```json
{
  "instructions": [{
    "kind": "removeExcludedUsers",
    "values": [ "user-key-123abc", "user-key-456def" ]
  }]
}
```

#### updateName<a id="updatename"></a>

Updates the name of the segment.

##### Parameters<a id="parameters"></a>

- `value`: Name of the segment.

Here's an example:

```json
{
  "instructions": [{
    "kind": "updateName",
    "value": "Updated segment name"
  }]
}
```

</details>

## Using JSON patches on a segment<a id="using-json-patches-on-a-segment"></a>

If you do not include the header described above, you can use a [JSON patch](https://apidocs.launchdarkly.com) or [JSON merge patch](https://datatracker.ietf.org/doc/html/rfc7386) representation of the desired changes.

For example, to update the description for a segment with a JSON patch, use the following request body:

```json
{
  "patch": [
    {
      "op": "replace",
      "path": "/description",
      "value": "new description"
    }
  ]
}
```

To update fields in the segment that are arrays, set the `path` to the name of the field and then append `/<array index>`. Use `/0` to add the new entry to the beginning of the array. Use `/-` to add the new entry to the end of the array.

For example, to add a rule to a segment, use the following request body:

```json
{
  "patch":[
    {
      "op": "add",
      "path": "/rules/0",
      "value": {
        "clauses": [{ "contextKind": "user", "attribute": "email", "op": "endsWith", "values": [".edu"], "negate": false }]
      }
    }
  ]
}
```

To add or remove targets from segments, we recommend using semantic patch. Semantic patch for segments includes specific instructions for adding and removing both included and excluded targets.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
update_semantic_patch_response = launchdarkly.segments.update_semantic_patch(
    patch=[
        {
            "op": "replace",
            "path": "/exampleField",
            "value": None,
        }
    ],
    project_key="projectKey_example",
    environment_key="environmentKey_example",
    segment_key="segmentKey_example",
    comment="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### patch: [`JSONPatch`](./launch_darkly_python_sdk/type/json_patch.py)<a id="patch-jsonpatchlaunch_darkly_python_sdktypejson_patchpy"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

##### segment_key: `str`<a id="segment_key-str"></a>

The segment key

##### comment: `str`<a id="comment-str"></a>

Optional comment

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`PatchWithComment`](./launch_darkly_python_sdk/type/patch_with_comment.py)
#### 🔄 Return<a id="🔄-return"></a>

[`UserSegment`](./launch_darkly_python_sdk/pydantic/user_segment.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/segments/{projectKey}/{environmentKey}/{segmentKey}` `patch`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.segments.update_user_context_targets`<a id="launchdarklysegmentsupdate_user_context_targets"></a>

Update user context targets included or excluded in a big segment. Big segments include larger list-based segments and synced segments. This operation does not support standard segments.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
launchdarkly.segments.update_user_context_targets(
    project_key="projectKey_example",
    environment_key="environmentKey_example",
    segment_key="segmentKey_example",
    included={
    },
    excluded={
    },
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

##### segment_key: `str`<a id="segment_key-str"></a>

The segment key

##### included: [`SegmentUserList`](./launch_darkly_python_sdk/type/segment_user_list.py)<a id="included-segmentuserlistlaunch_darkly_python_sdktypesegment_user_listpy"></a>


##### excluded: [`SegmentUserList`](./launch_darkly_python_sdk/type/segment_user_list.py)<a id="excluded-segmentuserlistlaunch_darkly_python_sdktypesegment_user_listpy"></a>


#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`SegmentUserState`](./launch_darkly_python_sdk/type/segment_user_state.py)
#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/segments/{projectKey}/{environmentKey}/{segmentKey}/users` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.segments_(beta).get_big_segment_export_info`<a id="launchdarklysegments_betaget_big_segment_export_info"></a>

Returns information about a big segment export process. This is an export for a synced segment or a list-based segment that can include more than 15,000 entries.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_big_segment_export_info_response = launchdarkly.segments_(beta).get_big_segment_export_info(
    project_key="projectKey_example",
    environment_key="environmentKey_example",
    segment_key="segmentKey_example",
    export_id="exportID_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

##### segment_key: `str`<a id="segment_key-str"></a>

The segment key

##### export_id: `str`<a id="export_id-str"></a>

The export ID

#### 🔄 Return<a id="🔄-return"></a>

[`Export`](./launch_darkly_python_sdk/pydantic/export.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/segments/{projectKey}/{environmentKey}/{segmentKey}/exports/{exportID}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.segments_(beta).get_import_info`<a id="launchdarklysegments_betaget_import_info"></a>

Returns information about a big segment import process. This is the import of a list-based segment that can include more than 15,000 entries.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_import_info_response = launchdarkly.segments_(beta).get_import_info(
    project_key="projectKey_example",
    environment_key="environmentKey_example",
    segment_key="segmentKey_example",
    import_id="importID_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

##### segment_key: `str`<a id="segment_key-str"></a>

The segment key

##### import_id: `str`<a id="import_id-str"></a>

The import ID

#### 🔄 Return<a id="🔄-return"></a>

[`ModelImport`](./launch_darkly_python_sdk/pydantic/model_import.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/segments/{projectKey}/{environmentKey}/{segmentKey}/imports/{importID}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.segments_(beta).start_big_segment_export`<a id="launchdarklysegments_betastart_big_segment_export"></a>

Starts a new export process for a big segment. This is an export for a synced segment or a list-based segment that can include more than 15,000 entries.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
launchdarkly.segments_(beta).start_big_segment_export(
    project_key="projectKey_example",
    environment_key="environmentKey_example",
    segment_key="segmentKey_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

##### segment_key: `str`<a id="segment_key-str"></a>

The segment key

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/segments/{projectKey}/{environmentKey}/{segmentKey}/exports` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.segments_(beta).start_big_segment_import`<a id="launchdarklysegments_betastart_big_segment_import"></a>

Start a new import process for a big segment. This is an import for a list-based segment that can include more than 15,000 entries.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
launchdarkly.segments_(beta).start_big_segment_import(
    project_key="projectKey_example",
    environment_key="environmentKey_example",
    segment_key="segmentKey_example",
    file=open('/path/to/file', 'rb'),
    mode="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

##### segment_key: `str`<a id="segment_key-str"></a>

The segment key

##### file: `IO`<a id="file-io"></a>

CSV file containing keys

##### mode: `str`<a id="mode-str"></a>

Import mode. Use either `merge` or `replace`

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`SegmentsBetaStartBigSegmentImportRequest`](./launch_darkly_python_sdk/type/segments_beta_start_big_segment_import_request.py)
#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/segments/{projectKey}/{environmentKey}/{segmentKey}/imports` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.tags.list`<a id="launchdarklytagslist"></a>

Get a list of tags.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_response = launchdarkly.tags.list(
    kind="string_example",
    pre="string_example",
    archived=True,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### kind: `str`<a id="kind-str"></a>

Fetch tags associated with the specified resource type. Options are `flag`, `project`, `environment`, `segment`. Returns all types by default.

##### pre: `str`<a id="pre-str"></a>

Return tags with the specified prefix

##### archived: `bool`<a id="archived-bool"></a>

Whether or not to return archived flags

#### 🔄 Return<a id="🔄-return"></a>

[`TagCollection`](./launch_darkly_python_sdk/pydantic/tag_collection.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/tags` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.teams.add_multiple_members_to_team`<a id="launchdarklyteamsadd_multiple_members_to_team"></a>

Add multiple members to an existing team by uploading a CSV file of member email addresses. Your CSV file must include email addresses in the first column. You can include data in additional columns, but LaunchDarkly ignores all data outside the first column. Headers are optional. To learn more, read [Managing team members](https://docs.launchdarkly.com/home/teams/managing#managing-team-members).

**Members are only added on a `201` response.** A `207` indicates the CSV file contains a combination of valid and invalid entries. A `207` results in no members being added to the team.

On a `207` response, if an entry contains bad input, the `message` field contains the row number as well as the reason for the error. The `message` field is omitted if the entry is valid.

Example `207` response:
```json
{
  "items": [
    {
      "status": "success",
      "value": "new-team-member@acme.com"
    },
    {
      "message": "Line 2: empty row",
      "status": "error",
      "value": ""
    },
    {
      "message": "Line 3: email already exists in the specified team",
      "status": "error",
      "value": "existing-team-member@acme.com"
    },
    {
      "message": "Line 4: invalid email formatting",
      "status": "error",
      "value": "invalid email format"
    }
  ]
}
```

Message | Resolution
--- | ---
Empty row | This line is blank. Add an email address and try again.
Duplicate entry | This email address appears in the file twice. Remove the email from the file and try again.
Email already exists in the specified team | This member is already on your team. Remove the email from the file and try again.
Invalid formatting | This email address is not formatted correctly. Fix the formatting and try again.
Email does not belong to a LaunchDarkly member | The email address doesn't belong to a LaunchDarkly account member. Invite them to LaunchDarkly, then re-add them to the team.

On a `400` response, the `message` field may contain errors specific to this endpoint.

Example `400` response:
```json
{
  "code": "invalid_request",
  "message": "Unable to process file"
}
```

Message | Resolution
--- | ---
Unable to process file | LaunchDarkly could not process the file for an unspecified reason. Review your file for errors and try again.
File exceeds 25mb | Break up your file into multiple files of less than 25mbs each.
All emails have invalid formatting | None of the email addresses in the file are in the correct format. Fix the formatting and try again.
All emails belong to existing team members | All listed members are already on this team. Populate the file with member emails that do not belong to the team and try again.
File is empty | The CSV file does not contain any email addresses. Populate the file and try again.
No emails belong to members of your LaunchDarkly organization | None of the email addresses belong to members of your LaunchDarkly account. Invite these members to LaunchDarkly, then re-add them to the team.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
add_multiple_members_to_team_response = launchdarkly.teams.add_multiple_members_to_team(
    team_key="teamKey_example",
    file=open('/path/to/file', 'rb'),
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### team_key: `str`<a id="team_key-str"></a>

The team key

##### file: `IO`<a id="file-io"></a>

CSV file containing email addresses

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`TeamsAddMultipleMembersToTeamRequest`](./launch_darkly_python_sdk/type/teams_add_multiple_members_to_team_request.py)
#### 🔄 Return<a id="🔄-return"></a>

[`TeamImportsRep`](./launch_darkly_python_sdk/pydantic/team_imports_rep.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/teams/{teamKey}/members` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.teams.create_team`<a id="launchdarklyteamscreate_team"></a>

Create a team. To learn more, read [Creating a team](https://docs.launchdarkly.com/home/teams/creating).

### Expanding the teams response<a id="expanding-the-teams-response"></a>
LaunchDarkly supports four fields for expanding the "Create team" response. By default, these fields are **not** included in the response.

To expand the response, append the `expand` query parameter and add a comma-separated list with any of the following fields:

* `members` includes the total count of members that belong to the team.
* `roles` includes a paginated list of the custom roles that you have assigned to the team.
* `projects` includes a paginated list of the projects that the team has any write access to.
* `maintainers` includes a paginated list of the maintainers that you have assigned to the team.

For example, `expand=members,roles` includes the `members` and `roles` fields in the response.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
create_team_response = launchdarkly.teams.create_team(
    key="team-key-123abc",
    name="Example team",
    description="An example team",
    custom_role_keys=["example-role1", "example-role2"],
    member_ids=["12ab3c45de678910fgh12345"],
    permission_grants=[
        {
            "action_set": "maintainTeam",
            "actions": ["updateTeamMembers"],
            "member_ids": ["12ab3c45de678910fgh12345"],
        }
    ],
    expand="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### key: `str`<a id="key-str"></a>

The team key

##### name: `str`<a id="name-str"></a>

A human-friendly name for the team

##### description: `str`<a id="description-str"></a>

A description of the team

##### custom_role_keys: [`TeamPostInputCustomRoleKeys`](./launch_darkly_python_sdk/type/team_post_input_custom_role_keys.py)<a id="custom_role_keys-teampostinputcustomrolekeyslaunch_darkly_python_sdktypeteam_post_input_custom_role_keyspy"></a>

##### member_ids: [`TeamPostInputMemberIDs`](./launch_darkly_python_sdk/type/team_post_input_member_ids.py)<a id="member_ids-teampostinputmemberidslaunch_darkly_python_sdktypeteam_post_input_member_idspy"></a>

##### permission_grants: List[`PermissionGrantInput`]<a id="permission_grants-listpermissiongrantinput"></a>

A list of permission grants. Permission grants allow access to a specific action, without having to create or update a custom role.

##### expand: `str`<a id="expand-str"></a>

A comma-separated list of properties that can reveal additional information in the response. Supported fields are explained above.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`TeamPostInput`](./launch_darkly_python_sdk/type/team_post_input.py)
#### 🔄 Return<a id="🔄-return"></a>

[`Team`](./launch_darkly_python_sdk/pydantic/team.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/teams` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.teams.get_by_team_key`<a id="launchdarklyteamsget_by_team_key"></a>

Fetch a team by key.

### Expanding the teams response<a id="expanding-the-teams-response"></a>
LaunchDarkly supports four fields for expanding the "Get team" response. By default, these fields are **not** included in the response.

To expand the response, append the `expand` query parameter and add a comma-separated list with any of the following fields:

* `members` includes the total count of members that belong to the team.
* `roles` includes a paginated list of the custom roles that you have assigned to the team.
* `projects` includes a paginated list of the projects that the team has any write access to.
* `maintainers` includes a paginated list of the maintainers that you have assigned to the team.

For example, `expand=members,roles` includes the `members` and `roles` fields in the response.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_by_team_key_response = launchdarkly.teams.get_by_team_key(
    team_key="teamKey_example",
    expand="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### team_key: `str`<a id="team_key-str"></a>

The team key.

##### expand: `str`<a id="expand-str"></a>

A comma-separated list of properties that can reveal additional information in the response.

#### 🔄 Return<a id="🔄-return"></a>

[`Team`](./launch_darkly_python_sdk/pydantic/team.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/teams/{teamKey}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.teams.get_custom_roles`<a id="launchdarklyteamsget_custom_roles"></a>

Fetch the custom roles that have been assigned to the team. To learn more, read [Managing team permissions](https://docs.launchdarkly.com/home/teams/managing#managing-team-permissions).

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_custom_roles_response = launchdarkly.teams.get_custom_roles(
    team_key="teamKey_example",
    limit=1,
    offset=1,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### team_key: `str`<a id="team_key-str"></a>

The team key

##### limit: `int`<a id="limit-int"></a>

The number of roles to return in the response. Defaults to 20.

##### offset: `int`<a id="offset-int"></a>

Where to start in the list. This is for use with pagination. For example, an offset of 10 skips the first ten items and then returns the next items in the list, up to the query `limit`.

#### 🔄 Return<a id="🔄-return"></a>

[`TeamCustomRoles`](./launch_darkly_python_sdk/pydantic/team_custom_roles.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/teams/{teamKey}/roles` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.teams.get_maintainers`<a id="launchdarklyteamsget_maintainers"></a>

Fetch the maintainers that have been assigned to the team. To learn more, read [Managing team maintainers](https://docs.launchdarkly.com/home/teams/managing#managing-team-maintainers).

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_maintainers_response = launchdarkly.teams.get_maintainers(
    team_key="teamKey_example",
    limit=1,
    offset=1,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### team_key: `str`<a id="team_key-str"></a>

The team key

##### limit: `int`<a id="limit-int"></a>

The number of maintainers to return in the response. Defaults to 20.

##### offset: `int`<a id="offset-int"></a>

Where to start in the list. This is for use with pagination. For example, an offset of 10 skips the first ten items and then returns the next items in the list, up to the query `limit`.

#### 🔄 Return<a id="🔄-return"></a>

[`TeamMaintainers`](./launch_darkly_python_sdk/pydantic/team_maintainers.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/teams/{teamKey}/maintainers` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.teams.list_teams`<a id="launchdarklyteamslist_teams"></a>

Return a list of teams.

By default, this returns the first 20 teams. Page through this list with the `limit` parameter and by following the `first`, `prev`, `next`, and `last` links in the `_links` field that returns. If those links do not appear, the pages they refer to don't exist. For example, the `first` and `prev` links will be missing from the response on the first page, because there is no previous page and you cannot return to the first page when you are already on the first page.

### Filtering teams<a id="filtering-teams"></a>

LaunchDarkly supports the following fields for filters:

- `query` is a string that matches against the teams' names and keys. It is not case-sensitive.
  - A request with `query:abc` returns teams with the string `abc` in their name or key.
- `nomembers` is a boolean that filters the list of teams who have 0 members
  - A request with `nomembers:true` returns teams that have 0 members
  - A request with `nomembers:false` returns teams that have 1 or more members

### Expanding the teams response<a id="expanding-the-teams-response"></a>
LaunchDarkly supports four fields for expanding the "List teams" response. By default, these fields are **not** included in the response.

To expand the response, append the `expand` query parameter and add a comma-separated list with any of the following fields:

* `members` includes the total count of members that belong to the team.
* `roles` includes a paginated list of the custom roles that you have assigned to the team.
* `projects` includes a paginated list of the projects that the team has any write access to.
* `maintainers` includes a paginated list of the maintainers that you have assigned to the team.

For example, `expand=members,roles` includes the `members` and `roles` fields in the response.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_teams_response = launchdarkly.teams.list_teams(
    limit=1,
    offset=1,
    filter="string_example",
    expand="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### limit: `int`<a id="limit-int"></a>

The number of teams to return in the response. Defaults to 20.

##### offset: `int`<a id="offset-int"></a>

Where to start in the list. Use this with pagination. For example, an offset of 10 skips the first ten items and returns the next `limit` items.

##### filter: `str`<a id="filter-str"></a>

A comma-separated list of filters. Each filter is constructed as `field:value`.

##### expand: `str`<a id="expand-str"></a>

A comma-separated list of properties that can reveal additional information in the response.

#### 🔄 Return<a id="🔄-return"></a>

[`Teams`](./launch_darkly_python_sdk/pydantic/teams.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/teams` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.teams.remove_by_team_key`<a id="launchdarklyteamsremove_by_team_key"></a>

Delete a team by key. To learn more, read [Deleting a team](https://docs.launchdarkly.com/home/teams/managing#deleting-a-team).

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
launchdarkly.teams.remove_by_team_key(
    team_key="teamKey_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### team_key: `str`<a id="team_key-str"></a>

The team key

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/teams/{teamKey}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.teams.update_semantic_patch`<a id="launchdarklyteamsupdate_semantic_patch"></a>

Perform a partial update to a team. Updating a team uses the semantic patch format.

To make a semantic patch request, you must append `domain-model=launchdarkly.semanticpatch` to your `Content-Type` header. To learn more, read [Updates using semantic patch](https://apidocs.launchdarkly.com).

### Instructions<a id="instructions"></a>

Semantic patch requests support the following `kind` instructions for updating teams.

<details>
<summary>Click to expand instructions for <strong>updating teams</strong></summary>

#### addCustomRoles<a id="addcustomroles"></a>

Adds custom roles to the team. Team members will have these custom roles granted to them.

##### Parameters<a id="parameters"></a>

- `values`: List of custom role keys.

Here's an example:

```json
{
  "instructions": [{
    "kind": "addCustomRoles",
    "values": [ "example-custom-role" ]
  }]
}
```

#### removeCustomRoles<a id="removecustomroles"></a>

Removes custom roles from the team. The app will no longer grant these custom roles to the team members.

##### Parameters<a id="parameters"></a>

- `values`: List of custom role keys.

Here's an example:

```json
{
  "instructions": [{
    "kind": "removeCustomRoles",
    "values": [ "example-custom-role" ]
  }]
}
```

#### addMembers<a id="addmembers"></a>

Adds members to the team.

##### Parameters<a id="parameters"></a>

- `values`: List of member IDs to add.

Here's an example:

```json
{
  "instructions": [{
    "kind": "addMembers",
    "values": [ "1234a56b7c89d012345e678f", "507f1f77bcf86cd799439011" ]
  }]
}
```

#### removeMembers<a id="removemembers"></a>

Removes members from the team.

##### Parameters<a id="parameters"></a>

- `values`: List of member IDs to remove.

Here's an example:

```json
{
  "instructions": [{
    "kind": "removeMembers",
    "values": [ "1234a56b7c89d012345e678f", "507f1f77bcf86cd799439011" ]
  }]
}
```

#### replaceMembers<a id="replacemembers"></a>

Replaces the existing members of the team with the new members.

##### Parameters<a id="parameters"></a>

- `values`: List of member IDs of the new members.

Here's an example:

```json
{
  "instructions": [{
    "kind": "replaceMembers",
    "values": [ "1234a56b7c89d012345e678f", "507f1f77bcf86cd799439011" ]
  }]
}
```

#### addPermissionGrants<a id="addpermissiongrants"></a>

Adds permission grants to members for the team. For example, a permission grant could allow a member to act as a team maintainer. A permission grant may have either an `actionSet` or a list of `actions` but not both at the same time. The members do not have to be team members to have a permission grant for the team.

##### Parameters<a id="parameters"></a>

- `actionSet`: Name of the action set.
- `actions`: List of actions.
- `memberIDs`: List of member IDs.

Here's an example:

```json
{
  "instructions": [{
    "kind": "addPermissionGrants",
    "actions": [ "updateTeamName", "updateTeamDescription" ],
    "memberIDs": [ "1234a56b7c89d012345e678f", "507f1f77bcf86cd799439011" ]
  }]
}
```

#### removePermissionGrants<a id="removepermissiongrants"></a>

Removes permission grants from members for the team. A permission grant may have either an `actionSet` or a list of `actions` but not both at the same time. The `actionSet` and `actions` must match an existing permission grant.

##### Parameters<a id="parameters"></a>

- `actionSet`: Name of the action set.
- `actions`: List of actions.
- `memberIDs`: List of member IDs.

Here's an example:

```json
{
  "instructions": [{
    "kind": "removePermissionGrants",
    "actions": [ "updateTeamName", "updateTeamDescription" ],
    "memberIDs": [ "1234a56b7c89d012345e678f", "507f1f77bcf86cd799439011" ]
  }]
}
```

#### updateDescription<a id="updatedescription"></a>

Updates the description of the team.

##### Parameters<a id="parameters"></a>

- `value`: The new description.

Here's an example:

```json
{
  "instructions": [{
    "kind": "updateDescription",
    "value": "Updated team description"
  }]
}
```

#### updateName<a id="updatename"></a>

Updates the name of the team.

##### Parameters<a id="parameters"></a>

- `value`: The new name.

Here's an example:

```json
{
  "instructions": [{
    "kind": "updateName",
    "value": "Updated team name"
  }]
}
```

</details>

### Expanding the teams response<a id="expanding-the-teams-response"></a>
LaunchDarkly supports four fields for expanding the "Update team" response. By default, these fields are **not** included in the response.

To expand the response, append the `expand` query parameter and add a comma-separated list with any of the following fields:

* `members` includes the total count of members that belong to the team.
* `roles` includes a paginated list of the custom roles that you have assigned to the team.
* `projects` includes a paginated list of the projects that the team has any write access to.
* `maintainers` includes a paginated list of the maintainers that you have assigned to the team.

For example, `expand=members,roles` includes the `members` and `roles` fields in the response.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
update_semantic_patch_response = launchdarkly.teams.update_semantic_patch(
    instructions=[
        {
            "key": None,
        }
    ],
    team_key="teamKey_example",
    comment="Optional comment about the update",
    expand="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### instructions: [`Instructions`](./launch_darkly_python_sdk/type/instructions.py)<a id="instructions-instructionslaunch_darkly_python_sdktypeinstructionspy"></a>

##### team_key: `str`<a id="team_key-str"></a>

The team key

##### comment: `str`<a id="comment-str"></a>

Optional comment describing the update

##### expand: `str`<a id="expand-str"></a>

A comma-separated list of properties that can reveal additional information in the response. Supported fields are explained above.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`TeamPatchInput`](./launch_darkly_python_sdk/type/team_patch_input.py)
#### 🔄 Return<a id="🔄-return"></a>

[`Team`](./launch_darkly_python_sdk/pydantic/team.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/teams/{teamKey}` `patch`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.teams_(beta).update_multiple_teams_semantic_patch`<a id="launchdarklyteams_betaupdate_multiple_teams_semantic_patch"></a>

Perform a partial update to multiple teams. Updating teams uses the semantic patch format.

To make a semantic patch request, you must append `domain-model=launchdarkly.semanticpatch` to your `Content-Type` header. To learn more, read [Updates using semantic patch](https://apidocs.launchdarkly.com).

### Instructions<a id="instructions"></a>

Semantic patch requests support the following `kind` instructions for updating teams.

<details>
<summary>Click to expand instructions for <strong>updating teams</strong></summary>

#### addMembersToTeams<a id="addmemberstoteams"></a>

Add the members to teams.

##### Parameters<a id="parameters"></a>

- `memberIDs`: List of member IDs to add.
- `teamKeys`: List of teams to update.

Here's an example:

```json
{
  "instructions": [{
    "kind": "addMembersToTeams",
    "memberIDs": [
      "1234a56b7c89d012345e678f"
    ],
    "teamKeys": [
      "example-team-1",
      "example-team-2"
    ]
  }]
}
```

#### addAllMembersToTeams<a id="addallmemberstoteams"></a>

Add all members to the team. Members that match any of the filters are **excluded** from the update.

##### Parameters<a id="parameters"></a>

- `teamKeys`: List of teams to update.
- `filterLastSeen`: (Optional) A JSON object with one of the following formats:
  - `{"never": true}` - Members that have never been active, such as those who have not accepted their invitation to LaunchDarkly, or have not logged in after being provisioned via SCIM.
  - `{"noData": true}` - Members that have not been active since LaunchDarkly began recording last seen timestamps.
  - `{"before": 1608672063611}` - Members that have not been active since the provided value, which should be a timestamp in Unix epoch milliseconds.
- `filterQuery`: (Optional) A string that matches against the members' emails and names. It is not case sensitive.
- `filterRoles`: (Optional) A `|` separated list of roles and custom roles. For the purposes of this filtering, `Owner` counts as `Admin`.
- `filterTeamKey`: (Optional) A string that matches against the key of the team the members belong to. It is not case sensitive.
- `ignoredMemberIDs`: (Optional) A list of member IDs.

Here's an example:

```json
{
  "instructions": [{
    "kind": "addAllMembersToTeams",
    "teamKeys": [
      "example-team-1",
      "example-team-2"
    ],
    "filterLastSeen": { "never": true }
  }]
}
```

</details>


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
update_multiple_teams_semantic_patch_response = launchdarkly.teams_(beta).update_multiple_teams_semantic_patch(
    instructions=[
        {
            "key": None,
        }
    ],
    comment="Optional comment about the update",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### instructions: [`Instructions`](./launch_darkly_python_sdk/type/instructions.py)<a id="instructions-instructionslaunch_darkly_python_sdktypeinstructionspy"></a>

##### comment: `str`<a id="comment-str"></a>

Optional comment describing the update

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`TeamsPatchInput`](./launch_darkly_python_sdk/type/teams_patch_input.py)
#### 🔄 Return<a id="🔄-return"></a>

[`BulkEditTeamsRep`](./launch_darkly_python_sdk/pydantic/bulk_edit_teams_rep.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/teams` `patch`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.user_settings.get_user_expiring_flag_targets`<a id="launchdarklyuser_settingsget_user_expiring_flag_targets"></a>

Get a list of flags for which the given user is scheduled for removal.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_user_expiring_flag_targets_response = launchdarkly.user_settings.get_user_expiring_flag_targets(
    project_key="projectKey_example",
    user_key="userKey_example",
    environment_key="environmentKey_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### user_key: `str`<a id="user_key-str"></a>

The user key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

#### 🔄 Return<a id="🔄-return"></a>

[`ExpiringUserTargetGetResponse`](./launch_darkly_python_sdk/pydantic/expiring_user_target_get_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/users/{projectKey}/{userKey}/expiring-user-targets/{environmentKey}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.user_settings.list_flag_settings_for_user`<a id="launchdarklyuser_settingslist_flag_settings_for_user"></a>

Get the current flag settings for a given user. <br /><br />The `_value` is the flag variation that the user receives. The `setting` indicates whether you've explicitly targeted a user to receive a particular variation. For example, if you have turned off a feature flag for a user, this setting will be `false`. The example response indicates that the user `Abbie_Braun` has the `sort.order` flag enabled and the `alternate.page` flag disabled, and that the user has not been explicitly targeted to receive a particular variation.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_flag_settings_for_user_response = launchdarkly.user_settings.list_flag_settings_for_user(
    project_key="projectKey_example",
    environment_key="environmentKey_example",
    user_key="userKey_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

##### user_key: `str`<a id="user_key-str"></a>

The user key

#### 🔄 Return<a id="🔄-return"></a>

[`UserFlagSettings`](./launch_darkly_python_sdk/pydantic/user_flag_settings.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/users/{projectKey}/{environmentKey}/{userKey}/flags` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.user_settings.single_flag_setting`<a id="launchdarklyuser_settingssingle_flag_setting"></a>

Get a single flag setting for a user by flag key. <br /><br />The `_value` is the flag variation that the user receives. The `setting` indicates whether you've explicitly targeted a user to receive a particular variation. For example, if you have turned off a feature flag for a user, this setting will be `false`. The example response indicates that the user `Abbie_Braun` has the `sort.order` flag enabled.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
single_flag_setting_response = launchdarkly.user_settings.single_flag_setting(
    project_key="projectKey_example",
    environment_key="environmentKey_example",
    user_key="userKey_example",
    feature_flag_key="featureFlagKey_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

##### user_key: `str`<a id="user_key-str"></a>

The user key

##### feature_flag_key: `str`<a id="feature_flag_key-str"></a>

The feature flag key

#### 🔄 Return<a id="🔄-return"></a>

[`UserFlagSetting`](./launch_darkly_python_sdk/pydantic/user_flag_setting.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/users/{projectKey}/{environmentKey}/{userKey}/flags/{featureFlagKey}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.user_settings.update_expiring_user_target`<a id="launchdarklyuser_settingsupdate_expiring_user_target"></a>

Schedule the specified user for removal from individual targeting on one or more flags. The user must already be individually targeted for each flag.

You can add, update, or remove a scheduled removal date. You can only schedule a user for removal on a single variation per flag.

Updating an expiring target uses the semantic patch format. To make a semantic patch request, you must append `domain-model=launchdarkly.semanticpatch` to your `Content-Type` header. To learn more, read [Updates using semantic patch](https://apidocs.launchdarkly.com).

### Instructions<a id="instructions"></a>

Semantic patch requests support the following `kind` instructions for updating expiring user targets.

<details>
<summary>Click to expand instructions for <strong>updating expiring user targets</strong></summary>

#### addExpireUserTargetDate<a id="addexpireusertargetdate"></a>

Adds a date and time that LaunchDarkly will remove the user from the flag's individual targeting.

##### Parameters<a id="parameters"></a>

* `flagKey`: The flag key
* `variationId`: ID of a variation on the flag
* `value`: The time, in Unix milliseconds, when LaunchDarkly should remove the user from individual targeting for this flag.

#### updateExpireUserTargetDate<a id="updateexpireusertargetdate"></a>

Updates the date and time that LaunchDarkly will remove the user from the flag's individual targeting.

##### Parameters<a id="parameters"></a>

* `flagKey`: The flag key
* `variationId`: ID of a variation on the flag
* `value`: The time, in Unix milliseconds, when LaunchDarkly should remove the user from individual targeting for this flag.
* `version`: The version of the expiring user target to update. If included, update will fail if version doesn't match current version of the expiring user target.

#### removeExpireUserTargetDate<a id="removeexpireusertargetdate"></a>

Removes the scheduled removal of the user from the flag's individual targeting. The user will remain part of the flag's individual targeting until explicitly removed, or until another removal is scheduled.

##### Parameters<a id="parameters"></a>

* `flagKey`: The flag key
* `variationId`: ID of a variation on the flag

</details>


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
update_expiring_user_target_response = launchdarkly.user_settings.update_expiring_user_target(
    instructions=[
        {
            "version": 1,
            "kind": "addExpireUserTargetDate",
            "flag_key": "sample-flag-key",
            "variation_id": "ce12d345-a1b2-4fb5-a123-ab123d4d5f5d",
            "value": 1653469200000,
        }
    ],
    project_key="projectKey_example",
    user_key="userKey_example",
    environment_key="environmentKey_example",
    comment="optional comment",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### instructions: List[`InstructionUserRequest`]<a id="instructions-listinstructionuserrequest"></a>

The instructions to perform when updating

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### user_key: `str`<a id="user_key-str"></a>

The user key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

##### comment: `str`<a id="comment-str"></a>

Optional comment describing the change

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`PatchUsersRequest`](./launch_darkly_python_sdk/type/patch_users_request.py)
#### 🔄 Return<a id="🔄-return"></a>

[`ExpiringUserTargetPatchResponse`](./launch_darkly_python_sdk/pydantic/expiring_user_target_patch_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/users/{projectKey}/{userKey}/expiring-user-targets/{environmentKey}` `patch`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.user_settings.update_flag_settings_for_user`<a id="launchdarklyuser_settingsupdate_flag_settings_for_user"></a>

Enable or disable a feature flag for a user based on their key.

Omitting the `setting` attribute from the request body, or including a `setting` of `null`, erases the current setting for a user.

If you previously patched the flag, and the patch included the user's data, LaunchDarkly continues to use that data. If LaunchDarkly has never encountered the user's key before, it calculates the flag values based on the user key alone.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
launchdarkly.user_settings.update_flag_settings_for_user(
    project_key="projectKey_example",
    environment_key="environmentKey_example",
    user_key="userKey_example",
    feature_flag_key="featureFlagKey_example",
    setting=None,
    comment="make sure this context experiences a specific variation",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

##### user_key: `str`<a id="user_key-str"></a>

The user key

##### feature_flag_key: `str`<a id="feature_flag_key-str"></a>

The feature flag key

##### setting: [`Union[bool, date, datetime, dict, float, int, list, str, None]`](./launch_darkly_python_sdk/type/typing_union_bool_date_datetime_dict_float_int_list_str_none.py)<a id="setting-unionbool-date-datetime-dict-float-int-list-str-nonelaunch_darkly_python_sdktypetyping_union_bool_date_datetime_dict_float_int_list_str_nonepy"></a>

The variation value to set for the context. Must match the flag's variation type.

##### comment: `str`<a id="comment-str"></a>

Optional comment describing the change

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`ValuePut`](./launch_darkly_python_sdk/type/value_put.py)
#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/users/{projectKey}/{environmentKey}/{userKey}/flags/{featureFlagKey}` `put`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.users.delete_by_project_environment_key`<a id="launchdarklyusersdelete_by_project_environment_key"></a>

> ### Use contexts instead
>
> After you have upgraded your LaunchDarkly SDK to use contexts instead of users, you should use [Delete context instances](https://apidocs.launchdarkly.com) instead of this endpoint.

Delete a user by key.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
launchdarkly.users.delete_by_project_environment_key(
    project_key="projectKey_example",
    environment_key="environmentKey_example",
    user_key="userKey_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

##### user_key: `str`<a id="user_key-str"></a>

The user key

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/users/{projectKey}/{environmentKey}/{userKey}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.users.get_user_by_key`<a id="launchdarklyusersget_user_by_key"></a>

> ### Use contexts instead
>
> After you have upgraded your LaunchDarkly SDK to use contexts instead of users, you should use [Get context instances](https://apidocs.launchdarkly.com) instead of this endpoint.

Get a user by key. The `user` object contains all attributes sent in `variation` calls for that key.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_user_by_key_response = launchdarkly.users.get_user_by_key(
    project_key="projectKey_example",
    environment_key="environmentKey_example",
    user_key="userKey_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

##### user_key: `str`<a id="user_key-str"></a>

The user key

#### 🔄 Return<a id="🔄-return"></a>

[`UserRecord`](./launch_darkly_python_sdk/pydantic/user_record.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/users/{projectKey}/{environmentKey}/{userKey}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.users.list_environment_users`<a id="launchdarklyuserslist_environment_users"></a>

> ### Use contexts instead
>
> After you have upgraded your LaunchDarkly SDK to use contexts instead of users, you should use [Search for contexts](https://apidocs.launchdarkly.com) instead of this endpoint.

List all users in the environment. Includes the total count of users. This is useful for exporting all users in the system for further analysis.

Each page displays users up to a set `limit`. The default is 20. To page through, follow the `next` link in the `_links` object. To learn more, read [Representations](https://apidocs.launchdarkly.com).


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_environment_users_response = launchdarkly.users.list_environment_users(
    project_key="projectKey_example",
    environment_key="environmentKey_example",
    limit=1,
    search_after="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

##### limit: `int`<a id="limit-int"></a>

The number of elements to return per page

##### search_after: `str`<a id="search_after-str"></a>

Limits results to users with sort values after the value you specify. You can use this for pagination, but we recommend using the `next` link we provide instead.

#### 🔄 Return<a id="🔄-return"></a>

[`UsersRep`](./launch_darkly_python_sdk/pydantic/users_rep.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/users/{projectKey}/{environmentKey}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.users.search_users`<a id="launchdarklyuserssearch_users"></a>

> ### Use contexts instead
>
> After you have upgraded your LaunchDarkly SDK to use contexts instead of users, you should use [Search for context instances](https://apidocs.launchdarkly.com) instead of this endpoint.

Search users in LaunchDarkly based on their last active date, a user attribute filter set, or a search query.

An example user attribute filter set is `filter=firstName:Anna,activeTrial:false`. This matches users that have the user attribute `firstName` set to `Anna`, that also have the attribute `activeTrial` set to `false`.

To paginate through results, follow the `next` link in the `_links` object. To learn more, read [Representations](https://apidocs.launchdarkly.com).


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
search_users_response = launchdarkly.users.search_users(
    project_key="projectKey_example",
    environment_key="environmentKey_example",
    q="string_example",
    limit=1,
    offset=1,
    after=1,
    sort="string_example",
    search_after="string_example",
    filter="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

##### q: `str`<a id="q-str"></a>

Full-text search for users based on name, first name, last name, e-mail address, or key

##### limit: `int`<a id="limit-int"></a>

Specifies the maximum number of items in the collection to return (max: 50, default: 20)

##### offset: `int`<a id="offset-int"></a>

Deprecated, use `searchAfter` instead. Specifies the first item to return in the collection.

##### after: `int`<a id="after-int"></a>

A Unix epoch time in milliseconds specifying the maximum last time a user requested a feature flag from LaunchDarkly

##### sort: `str`<a id="sort-str"></a>

Specifies a field by which to sort. LaunchDarkly supports the `userKey` and `lastSeen` fields. Fields prefixed by a dash ( - ) sort in descending order.

##### search_after: `str`<a id="search_after-str"></a>

Limits results to users with sort values after the value you specify. You can use this for pagination, but we recommend using the `next` link we provide instead.

##### filter: `str`<a id="filter-str"></a>

A comma-separated list of user attribute filters. Each filter is in the form of attributeKey:attributeValue

#### 🔄 Return<a id="🔄-return"></a>

[`Users`](./launch_darkly_python_sdk/pydantic/users.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/user-search/{projectKey}/{environmentKey}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.users_(beta).get_all_in_use_user_attributes`<a id="launchdarklyusers_betaget_all_in_use_user_attributes"></a>

> ### Use contexts instead
>
> After you have upgraded your LaunchDarkly SDK to use contexts instead of users, you should use [Get context attribute names](https://apidocs.launchdarkly.com) instead of this endpoint.

Get all in-use user attributes in the specified environment. The set of in-use attributes typically consists of all attributes seen within the past 30 days.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_all_in_use_user_attributes_response = launchdarkly.users_(beta).get_all_in_use_user_attributes(
    project_key="projectKey_example",
    environment_key="environmentKey_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

#### 🔄 Return<a id="🔄-return"></a>

[`UserAttributeNamesRep`](./launch_darkly_python_sdk/pydantic/user_attribute_names_rep.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/user-attributes/{projectKey}/{environmentKey}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.webhooks.create_new_webhook`<a id="launchdarklywebhookscreate_new_webhook"></a>

Create a new webhook.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
create_new_webhook_response = launchdarkly.webhooks.create_new_webhook(
    url="http://www.example.com",
    sign=True,
    tags=[],
    name="Example hook",
    secret="frobozz",
    statements=[
        {
            "resources": ["proj/*:env/*:flag/*;testing-tag"],
            "actions": ["*"],
            "effect": "allow",
        }
    ],
    _true=True,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### url: `str`<a id="url-str"></a>

The URL of the remote webhook

##### sign: `bool`<a id="sign-bool"></a>

If sign is false, the webhook does not include a signature header, and the secret can be omitted.

##### tags: [`WebhookPostTags`](./launch_darkly_python_sdk/type/webhook_post_tags.py)<a id="tags-webhookposttagslaunch_darkly_python_sdktypewebhook_post_tagspy"></a>

##### name: `str`<a id="name-str"></a>

A human-readable name for your webhook

##### secret: `str`<a id="secret-str"></a>

If sign is true, and the secret attribute is omitted, LaunchDarkly automatically generates a secret for you.

##### statements: [`StatementPostList`](./launch_darkly_python_sdk/type/statement_post_list.py)<a id="statements-statementpostlistlaunch_darkly_python_sdktypestatement_post_listpy"></a>

##### _true: `bool`<a id="_true-bool"></a>

Whether or not this webhook is enabled.

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`WebhookPost`](./launch_darkly_python_sdk/type/webhook_post.py)
#### 🔄 Return<a id="🔄-return"></a>

[`Webhook`](./launch_darkly_python_sdk/pydantic/webhook.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/webhooks` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.webhooks.delete_by_id`<a id="launchdarklywebhooksdelete_by_id"></a>

Delete a webhook by ID.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
launchdarkly.webhooks.delete_by_id(
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

The ID of the webhook to delete

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/webhooks/{id}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.webhooks.get_single_by_id`<a id="launchdarklywebhooksget_single_by_id"></a>

Get a single webhook by ID.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_single_by_id_response = launchdarkly.webhooks.get_single_by_id(
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

The ID of the webhook

#### 🔄 Return<a id="🔄-return"></a>

[`Webhook`](./launch_darkly_python_sdk/pydantic/webhook.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/webhooks/{id}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.webhooks.list_webhooks`<a id="launchdarklywebhookslist_webhooks"></a>

Fetch a list of all webhooks.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_webhooks_response = launchdarkly.webhooks.list_webhooks()
```

#### 🔄 Return<a id="🔄-return"></a>

[`Webhooks`](./launch_darkly_python_sdk/pydantic/webhooks.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/webhooks` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.webhooks.update_settings_patch`<a id="launchdarklywebhooksupdate_settings_patch"></a>

Update a webhook's settings. Updating webhook settings uses a [JSON patch](https://datatracker.ietf.org/doc/html/rfc6902) representation of the desired changes. To learn more, read [Updates](https://apidocs.launchdarkly.com).

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
update_settings_patch_response = launchdarkly.webhooks.update_settings_patch(
    body=[{"op":"replace","path":"/on","value":false}],
    id="id_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### id: `str`<a id="id-str"></a>

The ID of the webhook to update

##### requestBody: [`JSONPatch`](./launch_darkly_python_sdk/type/json_patch.py)<a id="requestbody-jsonpatchlaunch_darkly_python_sdktypejson_patchpy"></a>

#### 🔄 Return<a id="🔄-return"></a>

[`Webhook`](./launch_darkly_python_sdk/pydantic/webhook.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/webhooks/{id}` `patch`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.workflow_templates.create_feature_flag_template`<a id="launchdarklyworkflow_templatescreate_feature_flag_template"></a>

Create a template for a feature flag workflow

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
create_feature_flag_template_response = launchdarkly.workflow_templates.create_feature_flag_template(
    key="string_example",
    description="string_example",
    name="string_example",
    workflow_id="string_example",
    stages=[
        {
            "name": "10% rollout on day 1",
            "execute_conditions_in_sequence": True,
            "conditions": [{
    "description": "Require example-team approval for final stage",
    "wait_duration": 2,
    "execute_now": False,
    "notify_member_ids": ["507f1f77bcf86cd799439011"],
    "notify_team_keys": ["example-team"],
}],
        }
    ],
    project_key="string_example",
    environment_key="string_example",
    flag_key="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### key: `str`<a id="key-str"></a>

##### description: `str`<a id="description-str"></a>

##### name: `str`<a id="name-str"></a>

##### workflow_id: `str`<a id="workflow_id-str"></a>

##### stages: List[`StageInput`]<a id="stages-liststageinput"></a>

##### project_key: `str`<a id="project_key-str"></a>

##### environment_key: `str`<a id="environment_key-str"></a>

##### flag_key: `str`<a id="flag_key-str"></a>

#### ⚙️ Request Body<a id="⚙️-request-body"></a>

[`CreateWorkflowTemplateInput`](./launch_darkly_python_sdk/type/create_workflow_template_input.py)
#### 🔄 Return<a id="🔄-return"></a>

[`WorkflowTemplateOutput`](./launch_darkly_python_sdk/pydantic/workflow_template_output.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/templates` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.workflow_templates.delete_template`<a id="launchdarklyworkflow_templatesdelete_template"></a>

Delete a workflow template

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
launchdarkly.workflow_templates.delete_template(
    template_key="templateKey_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### template_key: `str`<a id="template_key-str"></a>

The template key

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/templates/{templateKey}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.workflow_templates.list`<a id="launchdarklyworkflow_templateslist"></a>

Get workflow templates belonging to an account, or can optionally return templates_endpoints.workflowTemplateSummariesListingOutputRep when summary query param is true

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
list_response = launchdarkly.workflow_templates.list(
    summary=True,
    search="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### summary: `bool`<a id="summary-bool"></a>

Whether the entire template object or just a summary should be returned

##### search: `str`<a id="search-str"></a>

The substring in either the name or description of a template

#### 🔄 Return<a id="🔄-return"></a>

[`WorkflowTemplatesListingOutputRep`](./launch_darkly_python_sdk/pydantic/workflow_templates_listing_output_rep.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/templates` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.workflows.create_workflow`<a id="launchdarklyworkflowscreate_workflow"></a>

Create a workflow for a feature flag. You can create a workflow directly, or you can apply a template to create a new workflow.

### Creating a workflow<a id="creating-a-workflow"></a>

You can use the create workflow endpoint to create a workflow directly by adding a `stages` array to the request body.

For each stage, define the `name`, `conditions` when the stage should be executed, and `action` that describes the stage.

<details>
<summary>Click to expand example</summary>

_Example request body_
```json
{
  "name": "Progressive rollout starting in two days",
  "description": "Turn flag targeting on and increase feature rollout in 10% increments each day",
  "stages": [
    {
      "name": "10% rollout on day 1",
      "conditions": [
        {
          "kind": "schedule",
          "scheduleKind": "relative", // or "absolute"
              //  If "scheduleKind" is "absolute", set "executionDate";
              // "waitDuration" and "waitDurationUnit" will be ignored
          "waitDuration": 2,
          "waitDurationUnit": "calendarDay"
        },
        {
          "kind": "ld-approval",
          "notifyMemberIds": [ "507f1f77bcf86cd799439011" ],
          "notifyTeamKeys": [ "team-key-123abc" ]
        }
      ],
      "action": {
        "instructions": [
          {
            "kind": "turnFlagOn"
          },
          {
            "kind": "updateFallthroughVariationOrRollout",
            "rolloutWeights": {
              "452f5fb5-7320-4ba3-81a1-8f4324f79d49": 90000,
              "fc15f6a4-05d3-4aa4-a997-446be461345d": 10000
            }
          }
        ]
      }
    }
  ]
}
```
</details>

### Creating a workflow by applying a workflow template<a id="creating-a-workflow-by-applying-a-workflow-template"></a>

You can also create a workflow by applying a workflow template. If you pass a valid workflow template key as the `templateKey` query parameter with the request, the API will attempt to create a new workflow with the stages defined in the workflow template with the corresponding key.

#### Applicability of stages<a id="applicability-of-stages"></a>
Templates are created in the context of a particular flag in a particular environment in a particular project. However, because workflows created from a template can be applied to any project, environment, and flag, some steps of the workflow may need to be updated in order to be applicable for the target resource.

You can pass a `dryRun` query parameter to tell the API to return a report of which steps of the workflow template are applicable in the target project/environment/flag, and which will need to be updated. When the `dryRun` query parameter is present the response body includes a `meta` property that holds a list of parameters that could potentially be inapplicable for the target resource. Each of these parameters will include a `valid` field. You will need to update any invalid parameters in order to create the new workflow. You can do this using the `parameters` property, which overrides the workflow template parameters.

#### Overriding template parameters<a id="overriding-template-parameters"></a>
You can use the `parameters` property in the request body to tell the API to override the specified workflow template parameters with new values that are specific to your target project/environment/flag.

<details>
<summary>Click to expand example</summary>

_Example request body_
```json
{
	"name": "workflow created from my-template",
	"description": "description of my workflow",
	"parameters": [
		{
			"_id": "62cf2bc4cadbeb7697943f3b",
			"path": "/clauses/0/values",
			"default": {
				"value": ["updated-segment"]
			}
		},
		{
			"_id": "62cf2bc4cadbeb7697943f3d",
			"path": "/variationId",
			"default": {
				"value": "abcd1234-abcd-1234-abcd-1234abcd12"
			}
		}
	]
}
```
</details>

If there are any steps in the template that are not applicable to the target resource, the workflow will not be created, and the `meta` property will be included in the response body detailing which parameters need to be updated.


#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
create_workflow_response = launchdarkly.workflows.create_workflow(
    name="Progressive rollout starting in two days",
    project_key="projectKey_example",
    feature_flag_key="featureFlagKey_example",
    environment_key="environmentKey_example",
    description="Turn flag on for 10% of users each day",
    maintainer_id="string_example",
    stages=[
        {
            "name": "10% rollout on day 1",
            "execute_conditions_in_sequence": True,
            "conditions": [{
    "description": "Require example-team approval for final stage",
    "wait_duration": 2,
    "execute_now": False,
    "notify_member_ids": ["507f1f77bcf86cd799439011"],
    "notify_team_keys": ["example-team"],
}],
        }
    ],
    template_key="string_example",
    template_key="string_example",
    dry_run=True,
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### feature_flag_key: `str`<a id="feature_flag_key-str"></a>

The feature flag key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

##### template_key: `str`<a id="template_key-str"></a>

The template key to apply as a starting point for the new workflow

##### dry_run: `bool`<a id="dry_run-bool"></a>

Whether to call the endpoint in dry-run mode

##### requestBody: [`CustomWorkflowInput`](./launch_darkly_python_sdk/type/custom_workflow_input.py)<a id="requestbody-customworkflowinputlaunch_darkly_python_sdktypecustom_workflow_inputpy"></a>

#### 🔄 Return<a id="🔄-return"></a>

[`CustomWorkflowOutput`](./launch_darkly_python_sdk/pydantic/custom_workflow_output.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/projects/{projectKey}/flags/{featureFlagKey}/environments/{environmentKey}/workflows` `post`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.workflows.delete_from_feature_flag`<a id="launchdarklyworkflowsdelete_from_feature_flag"></a>

Delete a workflow from a feature flag.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
launchdarkly.workflows.delete_from_feature_flag(
    project_key="projectKey_example",
    feature_flag_key="featureFlagKey_example",
    environment_key="environmentKey_example",
    workflow_id="workflowId_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### feature_flag_key: `str`<a id="feature_flag_key-str"></a>

The feature flag key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

##### workflow_id: `str`<a id="workflow_id-str"></a>

The workflow id

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/projects/{projectKey}/flags/{featureFlagKey}/environments/{environmentKey}/workflows/{workflowId}` `delete`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.workflows.get_custom_workflow_by_id`<a id="launchdarklyworkflowsget_custom_workflow_by_id"></a>

Get a specific workflow by ID.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_custom_workflow_by_id_response = launchdarkly.workflows.get_custom_workflow_by_id(
    project_key="projectKey_example",
    feature_flag_key="featureFlagKey_example",
    environment_key="environmentKey_example",
    workflow_id="workflowId_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### feature_flag_key: `str`<a id="feature_flag_key-str"></a>

The feature flag key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

##### workflow_id: `str`<a id="workflow_id-str"></a>

The workflow ID

#### 🔄 Return<a id="🔄-return"></a>

[`CustomWorkflowOutput`](./launch_darkly_python_sdk/pydantic/custom_workflow_output.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/projects/{projectKey}/flags/{featureFlagKey}/environments/{environmentKey}/workflows/{workflowId}` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `launchdarkly.workflows.get_feature_flag_environments_workflows`<a id="launchdarklyworkflowsget_feature_flag_environments_workflows"></a>

Display workflows associated with a feature flag.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
get_feature_flag_environments_workflows_response = launchdarkly.workflows.get_feature_flag_environments_workflows(
    project_key="projectKey_example",
    feature_flag_key="featureFlagKey_example",
    environment_key="environmentKey_example",
    status="string_example",
    sort="string_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### project_key: `str`<a id="project_key-str"></a>

The project key

##### feature_flag_key: `str`<a id="feature_flag_key-str"></a>

The feature flag key

##### environment_key: `str`<a id="environment_key-str"></a>

The environment key

##### status: `str`<a id="status-str"></a>

Filter results by workflow status. Valid status filters are `active`, `completed`, and `failed`.

##### sort: `str`<a id="sort-str"></a>

A field to sort the items by. Prefix field by a dash ( - ) to sort in descending order. This endpoint supports sorting by `creationDate` or `stopDate`.

#### 🔄 Return<a id="🔄-return"></a>

[`CustomWorkflowsListingOutput`](./launch_darkly_python_sdk/pydantic/custom_workflows_listing_output.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/api/v2/projects/{projectKey}/flags/{featureFlagKey}/environments/{environmentKey}/workflows` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---


## Author<a id="author"></a>
This Python package is automatically generated by [Konfig](https://konfigthis.com)
