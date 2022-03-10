export function round(v: number, n: number): number{
    let e = 1;
    while(n){e *= 10;n--;}
    return Math.round(v * e) / e;
}

export interface PointData {
    x: number,
    y: number
}

export interface ProblemAnswer {
    u: PointData,
    v: PointData,
    dis: number
}

export function solveWithBackend(list: PointData[]) : Promise<{[propName: string]: ProblemAnswer}> {
    return new Promise((resolve, reject) => {
        fetch("/api/solve", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({data: list}),
        })
        .then((res) => res.json())
        .then((json) => {
            resolve(json)
        })
        .catch((e) => reject(e))
    });
}