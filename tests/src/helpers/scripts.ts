export class GlobalCounter {
    static counter: number = 0;

    static getNextNumber(): number {
        return ++GlobalCounter.counter;
    }

    static getNextEmail(): string {
        return GlobalCounter.getNextNumber() + '.email@gmail.com';
    }

    static getNextString(): string {
        return GlobalCounter.getNextNumber().toString();
    }
}
