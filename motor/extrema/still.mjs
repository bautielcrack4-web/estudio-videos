// Edición extrema: saca CUADROS sueltos de las piezas para que el director las mire antes de renderizarlas. Corre como el usuario sin claves.
// uso: node still.mjs <carpeta_public> <salida_dir> <archivo.json con [{id, cuadros:[n,…]}]>   → <salida>/<id>_<k>.png y <salida>/cuadros.json
import fs from 'fs'; import path from 'path'; import {fileURLToPath} from 'url';
import {bundle} from '@remotion/bundler'; import {renderStill, selectComposition, openBrowser} from '@remotion/renderer';
const [pub, outDir, pedido] = process.argv.slice(2);
const root = path.dirname(fileURLToPath(import.meta.url));
fs.mkdirSync(outDir, {recursive: true});
const res = {};
const guardar = () => fs.writeFileSync(path.join(outDir, 'cuadros.json'), JSON.stringify(res, null, 1));
try {
  const lista = JSON.parse(fs.readFileSync(pedido, 'utf8'));
  const serveUrl = await bundle({entryPoint: path.join(root, 'src/index.ts'), publicDir: path.resolve(pub), enableCaching: false});
  const browser = await openBrowser('chrome', {chromiumOptions: {gl: 'swangle'}});
  for (const {id, cuadros} of lista) {
    res[id] = {ok: true, n: 0};
    try {
      const composition = await selectComposition({serveUrl, id, puppeteerInstance: browser});
      for (let k = 0; k < cuadros.length; k++) {
        const frame = Math.max(0, Math.min(composition.durationInFrames - 1, Math.round(cuadros[k])));
        await renderStill({composition, serveUrl, frame, output: path.join(outDir, id + '_' + k + '.png'), imageFormat: 'png', scale: 0.5,
                           puppeteerInstance: browser, timeoutInMilliseconds: 90000});
        res[id].n = k + 1;
      }
    } catch (e) { res[id] = {ok: false, n: res[id].n, error: String(e.message || e).slice(0, 700)}; }
    console.log(id, JSON.stringify(res[id])); guardar();
  }
  await browser.close({silent: true});
} catch (e) { res._error = String(e.message || e).slice(0, 700); console.log('cuadros:', res._error); }
guardar();
