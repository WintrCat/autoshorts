export function objectToArguments(options: { [key: string]: string }) {
    return Object
        .entries(options)
        .map(entry => {
            entry[0] = "--" + entry[0];
            entry[1] = entry[1].toString();
            return entry;
        })
        .reduce((acc, entry) => acc.concat(entry) as [string, string]);
}