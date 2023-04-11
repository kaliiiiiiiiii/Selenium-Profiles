try{var done = arguments[0];}catch{var done = undefined}

function buffer2hex (buffer) {
    return [...new Uint8Array (buffer)]
        .map (b => b.toString (16).padStart (2, "0"))
        .join ("");
}

function headers2dict(headers){
    var my_dict = {};
    for (var pair of headers.entries()) {
            my_dict[pair[0]] = pair[1]};
    return my_dict}

async function get(url, options){
    try{
        var response = await fetch(url, options);
        var buffer = await response.arrayBuffer()
        var hex = buffer2hex(buffer)
        var parsed = {
            "HEX":hex,
            "headers":headers2dict(response.headers),
            "ok":response.ok,
            "status_code":response.status,
            "redirected":response.redirected,
            "status_text":response.statusText,
            "type":response.type,
            "url":response.url
            };
        var parsed = {"status":"200", "value":parsed}
        }catch(e){var parsed = {"status":"error", "stack":e.stack, "message":e.message}}
    return parsed;
}

function is_done(value){
    if(done){done(value)}else{console.log(value)}
}

try{get(%s, %s).then((parsed) => {is_done(parsed)})}catch(e){is_done(e)}