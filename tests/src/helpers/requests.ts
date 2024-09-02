namespace RQ {
    export namespace auth {
        export interface signin {
            email?: string;
            domain?: string;
            id?: number;
            password: string;
        }
    }
    export namespace test {
        export interface signup {
            firstName: string;
            email: string;
            password: string;
        }
    }
}

export default RQ;
