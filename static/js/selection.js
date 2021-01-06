let confirmSelection = function () {
    if (window.confirm('回答者を選出します。よろしいですか？')) {
        return true;
    } else {
        return false;
    }
}

let confirmGrantPoint = function () {
    return window.confirm('ポイント付与を行います。よろしいですか？');
}