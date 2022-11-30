let objectToInspect = window,
    result = [];
    while(objectToInspect !== null)
        { result = result.concat(Object.getOwnPropertyNames(objectToInspect));
        objectToInspect = Object.getPrototypeOf(objectToInspect); }
    result.forEach(p => p.match(/.+_.+_(Array|Promise|Symbol)/ig)
        &&delete window[p]&&console.log('removed',p))
