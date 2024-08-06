const ErrorCodes = {
    INTERNAL_SERVER_ERROR: 1,
    UNPROCESSABLE_ENTITY: 2,
    TOKEN_EXPIRED: 3,
    TOKEN_VALIDATION_FAILED: 4,
    ENTITY_NOT_FOUND: 5,
    INCORRECT_AUTH_HEADER_FOMAT: 6,
    ACCESS_DENIED: 7,
    NAME_ALREADY_TAKEN: 8
}

const SuperUser = {
    email: "root@gmail.com",
    password: "root"
}

export {SuperUser, ErrorCodes};
