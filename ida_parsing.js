// const isClipboardInstalled = !!navigator.clipboard;
const isClipboardInstalled = false;

const testdata = `data:0000000140003000 byte_140003000  db 0, 4Dh, 51h, 50h, 0EFh, 0FBh, 0C3h, 0CFh, 92h, 45h
.data:0000000140003000                                         ; DATA XREF: sub_140001000+40↑o
.data:000000014000300A                 db 4Dh, 0CFh, 0F5h, 4, 40h, 50h, 43h, 63h, 0Eh dup(10)`;

function sanitize(text) {
  text = text.trim();
  if (text.endsWith("h")) text = text.slice(0, -1);
  if (text === "0") return "00";
  else {
    if (text.startsWith("0")) text = text.slice(1);
    text = text.padStart(2, "0");
    return text;
  }
}

class Format {
  constructor(data, name = "arr") {
    this._data = [];
    this.data = [];
    this.name = name;
    let tmpData = [];

    data.split("\n").forEach((element) => {
      const tmp = element.match(/[a-zA-Z0-9]+ dup\([0-9]*\)|db.*$/g);
      if (tmp) tmpData.push(tmp[0].slice(3, tmp[0].length));
    });
    tmpData = tmpData.join(",");

    for (let item of tmpData.split(",")) {
      item = item.trim();
      if (item.includes("dup")) {
        let [val, count] = item.split(" ");
        count = parseInt(count.slice(4, -1));
        val = sanitize(val);
        for (let i = 0; i < count; i++) {
          this._data.push(val);
          this.data.push("0x" + val);
        }
      } else {
        item = sanitize(item);
        this._data.push(item);
        this.data.push("0x" + item);
      }
    }
  }

  _join(arr, sep = ", ") {
    return arr.join(sep);
  }

  python(short = true) {
    let result;
    if (short) {
      result = `${this.name} = bytes.fromhex('${this._join(this._data, " ")}')`;
    } else {
      result = `${this.name} = [${this._join(this.data)}]`;
    }
    return result;
  }

  c() {
    const result = `int ${this.name}[${this.data.length + 1}] = {${this._join(
      this.data
    )}};`;
    return result;
  }
}
