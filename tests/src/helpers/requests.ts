namespace RQ {
    export namespace auth {
        export interface signin {
            email?: string;
            domain?: string;
            id?: number;
            password: string;
        }
    }
    export namespace orgs {
        export interface get {
            id: number;
        }
    }
    export namespace users {
        export interface get_orgs {
            id: number;
        }
    }
    export namespace test {
        export interface signup {
            firstName: string;
            email: string;
            password: string;
        }
        export namespace orgs {
            export interface create {
                name: string;
            }
            export interface invite {
                organization_id: number;
                user_id: number
            }
        }
    }
}

export default RQ;
