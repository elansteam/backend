namespace RQ {
    export namespace auth {
        export interface signin {
            email?: string;
            domain?: string;
            id?: number;
            password: string;
        }
    }
    export namespace organizations {
        export interface get {
            id: number;
        }
    }
    export namespace users {
        export interface get_organizations {
            id: number;
        }
    }
    export namespace test {
        export interface signup {
            firstName: string;
            email: string;
            password: string;
        }
        export namespace organizations {
            export interface create {
                name: string;
            }
            export interface invite {
                organizationId: number;
                userId: number
            }
        }
    }
}

export default RQ;
