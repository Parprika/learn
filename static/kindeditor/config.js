KindEditor.ready(function (k) {
    window.editor = k.create("#id_content", {
        width: '700px',
        resizeType: 0,
        allowImageRemote: false,
        filePostName: "file",
        uploadJson: "/upload/",
        afterBlur: function () {
				this.sync();
            }
    });
});