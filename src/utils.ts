export function round(v: number, n: number): number{
    let e = 1;
    while(n){e *= 10;n--;}
    return Math.round(v * e) / e;
}