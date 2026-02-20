# 💰 Personal Financial Tracker — SIC 2025

Chatbot de finanzas personales con **Inteligencia Artificial** que registra ingresos y gastos mediante lenguaje natural, los clasifica automáticamente usando **SVM + DistilBERT**, y predice tu gasto mensual con **Regresión Polinómica**.

## ✨ Características

| Módulo                         | Descripción                                                                                                    |
| ------------------------------ | -------------------------------------------------------------------------------------------------------------- |
| 💬 **Chatbot Conversacional**  | Interacción en lenguaje natural con LLM (Ollama / LLaMA 3.2). El usuario declara gastos e ingresos libremente. |
| 🤖 **Clasificación en Tiempo Real** | Cada concepto se clasifica automáticamente en categoría usando SVM + DistilBERT embeddings.               |
| 🗄️ **Persistencia en SQLite** | Todas las transacciones se guardan en base de datos, consultables desde el historial.                          |
| 📊 **Análisis de Gastos**      | Resumen por categoría con barras de progreso + predictor de gasto mensual (Regresión Polinómica grado 2).      |
| 🎯 **Metas Financieras**       | Sliders interactivos para distribuir presupuesto por categoría + consejo del asesor IA.                        |
| 📥 **Exportar a Excel**        | Genera un `.xlsx` formateado con todas las transacciones registradas.                                          |

## 🏗️ Arquitectura

```
PersonalFinancialTracker_SIC2025/
│   configure.sh
│   docker-compose.yml
│   headers.txt
│   check_g4_efficient.py
│   install.sh
│   ollama.log
│   setup.sh
│   stop.sh
│   finanzas.xlsx
│   README.pdf
│   Backend
│   check_distribution.py
│   check_g4.py
│   start.sh
│   DataBase/
│   │   GASTOS_CLASIFICADOS2.csv
│   │   ConjuntoDatos.csv
│   │   archivo_modificado.csv
│   │   GASTOS.csv
│   │   DATOS_CLASIFICADOS.csv
│   │   dataset_gestor_gastos.csv
│   Backend&Algorithms/
│   │   run_synthetic_tests.py
│   │   Dockerfile
│   │   NLPBERT.py
│   │   le_entrenado.pkl
│   │   pca_entrenado.pkl
│   │   classifier.py
│   │   metrics_summary.png
│   │   requirements.txt
│   │   finanzas.db
│   │   database.py
│   │   llm_provider.py
│   │   predictor.py
│   │   modelo_svm_entrenado.pkl
│   │   RegresionPolinomica.py
│   │   server.py
│   │   SVM3.py
│   │   reportes/
│   │   │   Reporte_Financiero_2026-02-20_00-16-11.xlsx
│   chatbot-angular/
│   │   Dockerfile
│   │   tsconfig.app.json
│   │   tsconfig.spec.json
│   │   angular.json
│   │   package-lock.json
│   │   nginx.conf
│   │   package.json
│   │   tsconfig.json
│   │   ingresos_y_gastos.xlsx
│   │   public/
│   │   │   favicon.ico
│   │   src/
│   │   │   index.html
│   │   │   styles.css
│   │   │   main.ts
│   │   │   app/
│   │   │   │   app.component.spec.ts
│   │   │   │   app.component.css
│   │   │   │   app.routes.ts
│   │   │   │   app.component.ts
│   │   │   │   app.component.html
│   │   │   │   app.config.ts
│   │   │   │   shared/
│   │   │   │   analisis-gastos/
│   │   │   │   │   analisis-gastos.component.spec.ts
│   │   │   │   │   analisis-gastos.component.css
│   │   │   │   │   analisis-gastos.component.html
│   │   │   │   │   analisis-gastos.component.ts
│   │   │   │   contacto/
│   │   │   │   │   contacto.component.ts
│   │   │   │   │   contacto.component.html
│   │   │   │   │   contacto.component.spec.ts
│   │   │   │   │   contacto.component.css
│   │   │   │   historial/
│   │   │   │   │   historial.component.css
│   │   │   │   │   historial.component.spec.ts
│   │   │   │   │   historial.component.html
│   │   │   │   │   historial.component.ts
│   │   │   │   core/
│   │   │   │   │   services/
│   │   │   │   │   │   finanzas.service.ts
│   │   │   │   │   components/
│   │   │   │   │   │   topbar/
│   │   │   │   │   │   │   topbar.component.html
│   │   │   │   │   │   │   topbar.component.ts
│   │   │   │   │   │   │   topbar.component.css
│   │   │   │   │   │   sidebar/
│   │   │   │   │   │   │   sidebar.component.html
│   │   │   │   │   │   │   sidebar.component.css
│   │   │   │   │   │   │   sidebar.component.ts
│   │   │   │   chatbot/
│   │   │   │   │   chatbot.component.css
│   │   │   │   │   chatbot.component.spec.ts
│   │   │   │   │   chatbot.component.html
│   │   │   │   │   chatbot.component.ts
│   │   │   │   metas-financieras/
│   │   │   │   │   metas-financieras.component.css
│   │   │   │   │   metas-financieras.component.ts
│   │   │   │   │   metas-financieras.component.spec.ts
│   │   │   │   │   metas-financieras.component.html
│   │   │   assets/
│   │   │   │   samsung2.png
│   │   │   │   samsung4.png
│   │   │   │   ernesto.jpeg
│   │   │   │   samsung3.png
│   │   │   │   cesar.jpeg
│   │   │   │   samsung5.png
│   │   │   │   samsung.png
│   │   │   │   david.jpg
│   │   .angular/
│   │   │   cache/
│   │   │   │   19.2.4/
│   │   │   │   │   chatbot-angular/
│   │   │   │   │   │   angular-compiler.db
│   │   │   │   │   │   angular-compiler.db-lock
│   │   │   │   │   │   vite/
│   │   │   │   │   │   │   deps_ssr/
│   │   │   │   │   │   │   │   _metadata.json
│   │   │   │   │   │   │   │   package.json
│   │   │   │   │   │   │   deps/
│   │   │   │   │   │   │   │   chunk-YQPEOUL7.js.map
│   │   │   │   │   │   │   │   @angular_common.js.map
│   │   │   │   │   │   │   │   @angular_router.js
│   │   │   │   │   │   │   │   @angular_platform-browser.js
│   │   │   │   │   │   │   │   @angular_forms.js
│   │   │   │   │   │   │   │   @angular_core.js.map
│   │   │   │   │   │   │   │   chunk-WREBD6OA.js.map
│   │   │   │   │   │   │   │   chunk-WREBD6OA.js
│   │   │   │   │   │   │   │   chunk-7EKPPUJA.js
│   │   │   │   │   │   │   │   @angular_core.js
│   │   │   │   │   │   │   │   @angular_platform-browser.js.map
│   │   │   │   │   │   │   │   @angular_common_http.js
│   │   │   │   │   │   │   │   @angular_common_http.js.map
│   │   │   │   │   │   │   │   chunk-YQPEOUL7.js
│   │   │   │   │   │   │   │   chunk-2UDGYMIF.js.map
│   │   │   │   │   │   │   │   _metadata.json
│   │   │   │   │   │   │   │   @angular_forms.js.map
│   │   │   │   │   │   │   │   chunk-7EKPPUJA.js.map
│   │   │   │   │   │   │   │   @angular_common.js
│   │   │   │   │   │   │   │   chunk-2UDGYMIF.js
│   │   │   │   │   │   │   │   package.json
│   │   │   │   │   │   │   │   @angular_router.js.map
│   │   │   │   │   angular-webpack/
│   │   │   │   │   │   1ef4e78015f0b78eec80c7140338accbf45b2cb8/
│   │   │   │   │   │   │   index.pack
│   │   │   │   │   │   │   0.pack
│   │   │   │   │   babel-webpack/
│   │   │   │   │   │   99e20b3630794f84e6ce0cac0aa92168db2ff72dd5890e26d3415ce71d5b5253.json
│   │   │   │   │   │   827a798aa7678f16b1f24808984161a17d4bf221ff5359a19fc5b93a51973a22.json
│   │   │   │   │   │   f70e5459a2c8e6951d24f43d0ebbb011ce01c0a8acca29b2892781122aa77cb8.json
│   │   │   │   │   │   da49099dbfdcfd7712370ff013de1273f62c497fe00139051ba9efcc29daa947.json
│   │   │   │   │   │   6bd6a25a8a6765130a2be9f60379f1a714650e2e23eb10454f7518b3e2d09f3d.json
│   │   │   │   │   │   4c47db73bdde0f6a5c6a2d6ff662141798e7cbed9d498ee77ffc958579ee74fc.json
│   │   │   │   │   │   1a41773c1f02e87378b5b3587acd563963a8c8c13ad5edf729c6d9f59ca570c6.json
│   │   │   │   │   │   cf595106895c2c6f8157e1f31b65142a529525146a54bb6d1fc31554b90790cd.json
│   │   │   │   │   │   1bb2d67b65542ecd976b474cea063f41afc6d77f96ba3e1dd37621a0d2347620.json
│   │   │   │   │   │   821233fa88d602bc087dbe1c1d973ca0a05376ae3c98813568443e4223bb279f.json
│   │   │   │   │   │   25e8aa46f9524d483428649b50ecabcb3cda06348371e15c61f92dda9fcdbad5.json
│   │   │   │   │   │   5a27769c3f92a23461b465ada06c3028b522fb6ddc44516c047e0d8d35f6b930.json
│   │   │   │   │   │   bd9e07b09846fcf177789f1ce9aaab4a0910dc29265613efbff35b2f75319b37.json
│   │   │   │   │   │   e1332970446d2e5a25ce716a5a762cead212c0f46258e6c1b8789d9322b1ba78.json
│   │   │   │   │   │   d7c56e185eaca62acb8435040ec95c4b0da54ef685cf536a80a90b1c01df6a12.json
│   │   │   │   │   │   4ddc9834b4554825c6021fbee9556025346e99286d1197eae68c6fa3822c910e.json
│   │   │   │   │   │   a55ae0ffd3df3960fa2aab4269ac83111d0f1de53cef3885598b24f0d9783eba.json
│   │   │   │   │   │   a61c5e65d2b2a340d8c8fa49adbe28a7339183970d8471d4626ed2628f48248d.json
│   │   │   │   │   │   e4bb20ca835351758e2ccad7f7fd962ee2b610dc29472acd57b24308ce53cffd.json
│   │   │   │   │   │   04283babf8047e057a01e4b77aad461be5a330c32839badab2009a90e65b7105.json
│   │   │   │   │   │   5d62c377eb82a1d0bd4a803075fa2a534a139265982a4f24664405479179250c.json
│   │   │   │   │   │   fb6c316d973363f174d25a8383fc5e61aa857b46d90be16a3aa529fb10f4df9b.json
│   │   │   │   │   │   4e6c851013234d46dc1ef1868873a90b7c97ea8c48b4372da9e352586c86b02f.json
│   │   │   │   │   │   baf33edb0822cf222ea01a4b4652f350c5b8cc7613804fa811493641adfd0768.json
│   │   │   │   │   │   6c909a6dc7da51b4cef68d8bc4becf124bcf86ff1c8d2992e3938c3a9c8c3be1.json
│   │   │   │   │   │   8f81e7f008770330aedf1716b0c5c845d3714b39f5984bb424dc48a712bd74f4.json
│   │   │   │   │   │   925ecb220b5c9d5e056b38d0890098d27cfdeb29785755a2683c4e01515d5003.json
│   │   │   │   │   │   a5dca428d6e15d77bb3eb3de03ed538a13d10a6b253551cc520ef36b02139188.json
│   │   │   │   │   │   342a6cc0cfbf2eacd1f56f94bd92515b40db1f427f272239807cb89966e36023.json
│   │   │   │   │   │   9ac83d5b76a4ab32fcd36dd9bcf5190647bf88532e053951f744d46846c7d578.json
│   │   │   │   │   │   76f583798f79b77d6cb4372944e29dd515273656ba045235fb602afff328fe31.json
│   │   │   │   │   │   2a5db9c35c6e9e98e1d185a8b6536cbd88ff8494af6ba651ea0fa6453f43437d.json
│   │   │   │   │   │   196cf311d02f135836da950c96041cde57690d0e540e7a974ab86d3a794c27f4.json
│   │   │   │   │   │   91de3bd43a6c9ad087a731537c1626d5c9ea9ec4ae2f3ac460a73431242dfa4a.json
│   │   │   │   │   │   30cb2806abb4f65e6e54e0b77d0cb62233692fedc7b86bf918eb542888ba99f1.json
│   │   │   │   │   │   4152be8af553d3dcacf456b315c231e81954c74cb1081c6b8979478648a73780.json
│   │   │   │   │   │   44a414403f38f249e9a0c3ece49f146e7616c934656e663f5aabf823ceac24d3.json
│   │   │   │   │   │   66a8883f7bb03673dab50f5076d24f16b04332c6d923c3ddf428cc41e22571fc.json
│   │   │   │   │   │   d9370b2ced80f2fdebe4395ed99bbe6b6cf6d502eb8969e538ec83590fd3d907.json
│   │   │   │   │   │   b6502a1aed328e7f0bc4d7eceed120187d917fd6fb12bdf53b5330c3e26583df.json
│   │   │   │   │   │   628275bc532f38426cfd857db5d4e1cd71318e1a25cae3781c0f5dd232fc0c9b.json
│   │   │   │   │   │   7ddc9e54b4bbfd272d81160fb724b96e8bde0218ea8f107eefea982733fa543d.json
│   │   │   │   │   │   80121a235dbe3fa9e7d11fe42fba7a2e7a80761e7c0d30b2e94099653e9fbc24.json
│   │   │   │   │   │   148e58644d272621451840dca9b8777b1b51429b2ed6dd3171d957641c334f24.json
│   │   │   │   │   │   89996354393dbc24b87d168178c5210a7d23d50179195f3449fe3254958a380c.json
│   │   │   │   │   │   4d53fbe87863217605e8ff67805407717609ee693142ae498f2f55c96208190e.json
│   │   │   │   │   │   e4e519940ab39daf5158c0cba9a4eee5fa193c0766cef228f53db971ee5532e4.json
│   │   │   │   │   │   a4109611f31044457204123790ac7186c326db29adf9e29940567c955b961ed0.json
│   │   │   │   │   │   9f1c8fd968a6f159dd59140d55eb5e9c66bf6bfecdb974be4433ed166f190435.json
│   │   │   │   │   │   38bb8dde45af36acfe45c404ed7cb1d1ff209b86faaf4acaa9fd1c850f48185f.json
│   │   │   │   │   │   bdc1c3ff8bc3520a6906e706a2fbc97d8c9319071644bd64b88803eb6a03884d.json
│   │   │   │   │   │   48be752dba4e0ae82ee6a72cd9b7ed13d1154d8768d18cfcde3506fb0ccffbe9.json
│   │   │   │   │   │   d1f62f65901c7d0cbc1f26ec4428c52a634dc4670890c99e9f644a1afcffb2a6.json
│   │   │   │   │   │   2c1474fced210953d81a708a2521def5269f29360c61ac4eb81aef3d7380bf15.json
│   │   │   │   │   │   ac96de5609ed1e1f52fd02948059a73dfbd7065375f5a90f7f8bab6aeae6504c.json
│   │   │   │   │   │   b96c74f7137899158fa016475ca3d3c339500e1c74538eb68563fff9564524ff.json
│   │   │   │   │   │   0213ecd26176b0005bdf4a140f9aeae9947b1935d75620aabea22c59ded85552.json
│   │   │   │   │   │   1332e52b11dde440a9fede9407a39953e331a549b3c2e452f84430c68700d068.json
│   │   │   │   │   │   dc43312b10943c62bc34f3dfdcb3642000deaa6457b83f050bd68b2335375fd3.json
│   │   │   │   │   │   97ba149106470975c959684112e2ba52d14786e113ccd0eeee791511fe458623.json
│   │   │   │   │   │   8c6b0d4c90afff099ee38814b6ff47ef865789f99a6a7435d62eb01782541417.json
│   │   │   │   │   │   75140eec6d4e07fbbf84846a9e45573866609882e90b7fa115428cece3e48d89.json
│   │   │   │   │   │   f6c9d1f083437b3a8f199ccb62941a4dbcb3caa3a1ab9501ffff42847f39c787.json
│   │   │   │   │   │   5c89340767a0d2799cbeb67957d9c57b86b5755760858bb86e4822c6996be8c5.json
│   │   │   │   │   │   f283592b1f549406cf8fb13a0db97f4cdac859c1b48dbb15b193a85abca3edcd.json
│   │   │   │   │   │   6892ab1e6f36aef9d1f58d2121dc6eb979915e8087220b2e9005faf40463a086.json
│   │   │   │   │   │   9a4b878a85936ca51cf993bf3c264b1327a205511ea35650a0be6ca5071b6e2f.json
│   │   │   │   │   │   5a9991f4cff66b98385390afa1422c81567852aae7f96590402e25433837a486.json
│   │   │   │   │   │   f6b9810a06b8edc8bfcdc405a4fc0c75d0b6c4e26539a986f0deaa17b3cd4854.json
│   │   │   │   │   │   ccbede545ce9797354de2761d6a7f7155a7773a6d3a78680c0685ca46dbdb185.json
│   │   │   │   │   │   46f9eebad7a6ba827f6b0b327c90b3a95cf56618080d796a2d9aabfc1c0d6649.json
│   │   │   │   │   │   56a7332289cb1113f5c7af3132eb23e70640847dee8cdac5c63b27ea058d7eb9.json
│   │   │   │   │   │   87ac9255ddebd0edbdedf79abb5f77a89441a0e812b59d69156242585343346c.json
│   │   │   │   │   │   d5b1f7cef932df1d07a9b8f123920fade916ef72d758cb256c7bd72c726ac186.json
│   │   │   │   │   │   2ad0af584c26d1fa57f13f5ab6d2c3aa14076e030c7ed0975e3711e9478f0ed9.json
│   │   │   │   │   │   c6953dac8eac637e1700ae1e4e5d64fbd4e3a57025b29749033b0e994a434c3c.json
│   │   │   │   │   │   db2e0b1abfa4f8ad888f673884fd17073ab717f92a567d351942aab74c0c323a.json
│   │   │   │   │   │   534250e23b5efe52f1e0d518a6180fbf43ef6af258e2c793e915b174ff295b4d.json
│   │   │   │   │   │   b7b874242f837a8546f4e1846ec7f78b4eb1c2e33c87606e4ed81059f9c55ae4.json
│   │   │   │   │   │   2d1e1116979cea0f385fb2a3d721bf9aecb5954b0b0fb5c4638b56f5c10e5c1d.json
│   │   │   │   │   │   797ac9ede5960fee5dd4ad3f5061539045348d3bbac2c6fdb18af79cd48311d7.json
│   │   │   │   │   │   aee60718956b6c1590cdd87d20ff66a06249801ea62fe4777df82b6feb844bd5.json
│   │   │   │   │   │   461cd8c1cf3e3799bbb08607f6e6a4f883773c733d28b897869ee89e80db3261.json
│   │   │   │   │   │   9ad43c3d41dfe53379bb1bd6a1e028eedcc24ec2b9ee44eb068bd9c3ee222ebb.json
│   │   │   │   │   │   91a3f3ea2192ecbef86db2820b8f3977f087d97e368d23378916371489e7d1c7.json
│   │   │   │   │   │   47dd03c52475c5099e0a9686cc93841ae8a42693286509ff76ea63cd7a61dd31.json
│   │   │   │   │   │   1bc095b6bb76c99d697fb00d6eb85b7348fced09e9427cf06bee3f0ea286cc80.json
│   │   │   │   │   │   a618ff1d0b15760377a10a4879394b13e2cf9c4e03f52aa3861cfefdab5da8ba.json
│   │   │   │   │   │   89f84c44a3a600b54afe98bc9e1f00a4778f5d2c9fe2ac4f18054bca1b31448e.json
│   │   │   │   │   │   77af31af89208b7cd4d88a9db7c5ca3fbcd8651982d3266b9fcbcae335338ad7.json
│   │   │   │   │   │   c6388b380fbd7d138c3c69ca6318f7ee57ec362ab8fd225877b9addf922c6051.json
│   │   │   │   │   │   3d2959d56751865e2e755b57abe30e5d1e0a4f4b9ccc4613e359f5462c21c36e.json
│   │   │   │   │   │   3686a11b0d863e96723a0715ef5f711da217f21e05dc6eb34ff221ba87d98f8d.json
│   │   │   │   │   │   8e4d321f6fe49bf3ecae9f20897442236a2e94a0fb80a0238854774f3da8b2fc.json
│   │   │   │   │   │   984d046a5e6aafa7587aae20b2790210ec9a13e527dee3f5f2187a531886a66d.json
│   │   │   │   │   │   90bdacb50923eb694dab61240c8c908690857ea5b46071f285b11cc2c1988b44.json
│   │   │   │   │   │   d10165923ea929fdfe329cf4cf954ccb00a6092183fecd4c6eafc1360eb0bca3.json
│   │   │   │   │   │   2a9464c1078ffdf280396bbf15a958ef907c9db35546af61d97b30fdf4f3c2ae.json
│   │   │   │   │   │   98449f95bea6f3422dc9632bacf77cd8c2e3d485b1371c5262a4dd60aab27844.json
│   │   │   │   │   │   32d5617b25d34767103109e5000c5700872d04af371c82202e8a73efc1e94e15.json
│   │   │   │   │   │   6233be4a93afc5bd8c40fdaed8129357fe57e72f5e0b48148a16b73f2bc01d13.json
│   │   │   │   │   │   a0519f100728f138af94c3470e09db45ddfaaa9068abd8f212cd4e4521cfc864.json
│   │   │   │   │   │   da3551e11ed4b22ff359da338bffd8fa8a6654527113efd139a9552142d6500d.json
│   │   │   │   │   │   a394678203e18c8af5fcd8403767ebe4a87d38d304cee0dfa32e0edc4b10c1e1.json
│   │   │   │   │   │   4a9c504bfa4b2f51ea640119db3f1d4f59f315995de91436e26eaa6fc0146aa8.json
│   │   │   │   │   │   51c0413cb0423db0bd4712230a6d38e4786a520293674a0b98beab079a38716e.json
│   │   │   │   │   │   0bd495e324289839fb8fe584830561a8e9c1a160a0aab5952e1ab4c76f134b75.json
│   │   │   │   │   │   d03e19e46faa998b1248486f8033dc03f01f6f620b2010e81ba26f862eb41879.json
│   │   │   │   │   │   b0c70ff39ad09dcaa50a6683460a41b4d1fcc139a2761c26b84fcc3cf35c87c9.json
│   │   │   │   │   │   2ae010c74a62826cdc1da5a96ab04f112ef092c51287d993c675f9918d5fc443.json
│   │   │   │   │   │   321b5c501c374d88b8c6a387186f6a906539606c621affecdc368837e6bcae35.json
│   │   │   │   │   │   9c7dfaf47c183a5bd32a9ce371e39b4d359c2bddad8f4c44494abda8c963acec.json
│   │   │   │   │   │   878a117f4d191102138360c6b86086eba930e8e66a1d5c6df419c82d5513466f.json
│   │   │   │   │   │   685447a328c429d975ab88c2ceb3ec89448db3a88f14e58449a750d90c14cd53.json
│   │   │   │   │   │   e4d08f829f0aba67fb22198aab9e36083dd7ddc3217825242a1dfff6427a3cf9.json
│   │   │   │   │   │   d85aad636d856770be9802dc2a2916ab8b34c59bc5e924f3dbdabec98b9739a5.json
│   │   │   │   │   │   18167dd1bcf07a0e4d066f51c5ecabff85ecefc4a43c53b5b23775ac36a69277.json
│   │   │   │   │   │   25c845754e38a338ad88b39f8d039413bdaa4ce94b73365b712e7e09ca6c282f.json
│   │   │   │   │   │   c3730a27320a34b53d370749beaca20b2b642ab4cdbccd50590f13d837d5038a.json
│   │   │   │   │   │   f164f446c716980a1c2e12a8011a9b257586135000d4df3640f537c423c2d222.json
│   │   │   │   │   │   a6ca29337109c16407f712c10ac6bfd6c895d2a7eddca7a528e3ec2f0fff92f7.json
│   │   │   │   │   │   b6818801f23609b44da337b880cf274785e3263eb5bd8855c501d3ad978e9f8a.json
│   │   │   │   │   │   f2dbd34df51c4fb28aded057b7f69db2ac35f51f0726ddc13940c728e1491316.json
│   │   │   │   │   │   c87cee281036b9f6ee18920168626c5850d83beb26095549f45d739718844d4d.json
│   │   │   │   │   │   2effa9ea4a916ff140bffd3cd127662cf2075597d8003966d7f518d8f9f21eb0.json
│   │   │   │   │   │   75ee3252c53e9a228a0b7fc1c5f99fa87f255f775524be2c94ec5c136e55b850.json
│   │   │   │   │   │   5958bf30a15b5e771639d5d00e4727895645751c321a255e9258706f4e28fa4b.json
│   │   │   │   │   │   40f86059865e8423a3142f51773d3d93c118b3890ea86999753943380e377839.json
│   │   │   │   │   │   7532374ea45a796524d428af2a0a2188d31f1ef6f6bc901ae660fcefec9a1fb4.json
│   │   │   │   │   │   bf9f6914bd3a0b08514a7121705c66bf33013d166b51506f0a45f56c5a333bd5.json
│   │   │   │   │   │   3c397c9546ef5c741de91ea7ca85e64efe47513cc7d8b269e3df5a2bc1dbfb08.json
│   │   │   │   │   │   379b917f6817ecae678286d89ee0cef6f37328e48ca6f452434441d5b48dc4e4.json
│   │   │   │   │   │   045286612d33ffe349ba6888c0226296e5a92156e69c2c1e7ffd82af8bdb48f4.json
│   │   │   │   │   │   d8743bcaf0aba27354529ab5f1c0e1c3235d3f3b71323106c8ec07ec36793b20.json
│   │   │   │   │   │   84885226a43e24c56c14cf00a6ca9accf03e623702498e2eec9917bb17c470fe.json
│   │   │   │   │   │   80cc425ecd78d5c3fd3b3fa3851bd9ee25294c33f9d3b9011327fa271ad57c3d.json
│   │   │   │   │   │   f961cd6cd04f031012ddfe9e25587c6a68e03d9f66bb1a6d4ba01a6804b3909e.json
│   │   │   │   │   │   8fa84caca65eec246357482ba169b5832e3c0e206f00b763f50efb3d8c49e74b.json
│   │   │   │   │   │   51a22bec1ae4ce0fc25f6e95527bb6d59f059baff9ecda267767e3ac8fbcf5ba.json
│   │   │   │   │   │   8e525999c15b6ab8b976bbd2f1a2e0ae03f5ef296485ffbba03e01cc852ba30e.json
│   │   │   │   │   │   576ea0ecb6756e358847275fe423d3fe606a609f69545f87bf74c68418059782.json
│   │   │   │   │   │   e8353976087f46248ffb6ab4ca749ce0f846c1627e8e38bfcd19e89fbbfb5769.json
│   │   │   │   │   │   ab03cabe2e29a3f58ac8c1d27e414a3e04aab6830cb3c9655e24392860eff2af.json
│   │   │   │   │   │   adec2d8254d27f5b0b20dcef15901b76730bc07fa075d501205af63d168ad3c9.json
│   │   │   │   │   │   4a039f478c580a7abed2213d4dd20e7b66a57e508cfb9a22959b1261b7da0dda.json
│   │   │   │   │   │   98cb27997d1c049a9eceda8ffdf5b74449489045244789092061dcb2b6b95369.json
│   │   │   │   │   │   3abd521541cbbde3a9bf95925a07fc340a250391da5b1fe757cba92b9ca0cc31.json
│   │   │   │   │   │   afd34f52a271e0b0453bfe88aacfa10d7eae3a1854f7c1b015dca2c502de2caa.json
│   │   │   │   │   │   738f77736cbd357dea98fd90434360c44e1ad14843c8edc307a77b4386209210.json
│   │   │   │   │   │   bc344064bce916199803cfdb6f295ca9595b244b75916fbea79bca89295fd31b.json
│   │   │   │   │   │   03545a5047636b8942aba1c9c70d938161154fe86d2cf4e15a56373f020c8b95.json
│   │   │   │   │   │   e2dda150ba9146d08ee27923226185e1e377bb0b1a866eb7a984ce899a6e8c28.json
│   │   │   │   │   │   2b21b8f3e003dee74ffcaaddaaaf0601a444c7b71ecd2bce8f8f8079f30bdca4.json
│   │   │   │   │   │   96884857a4afdc7645c8c5f3809491aaffc8dc5ffc5131e6ea2b1200ae742529.json
│   │   │   │   │   │   2be773e0b5b3ba3ef75105207d3d63f7c76545d4bb97eae8cec14c32dcaa72f8.json
│   │   │   │   │   │   25ee612d1e1fe6b5b006f99115c15919345baa6e6a4c6ba9f6e510765b96583a.json
│   │   │   │   │   │   11e92af5d8df7f58152da7edb34479f9f56f2a2a5f1b206287b52b354bc17457.json
│   │   │   │   │   │   683935116b1ae88ef124f503bea1dff1d96587c6a61fe1795b45fd702beb4b11.json
│   │   │   │   │   │   27a4c95664ae79f9bc8e2360208a5f7b6b8a7b89a3522523653d54427708f095.json
│   │   │   │   │   │   6634056d810a2e39107af796c0e54a2a6ba1fb94c7f97bd9f66d199fb389292e.json
│   │   │   │   │   │   75966b2864368fd0807cfcb6fc05cdc98cb60a37615b017fc4088dc5795c6946.json
│   │   │   │   │   │   3406a9fc0c06a6cf99cd0b29d436bffad1a57163e532d157431e13ef30133543.json
│   │   │   │   │   │   90b4e4b6ccbd5ff58b920622ade00608d21a2d856733866a16af2722324a20e3.json
│   │   │   │   │   │   a101db1dec08c3443b5460f9c623635256e65d6f8cc96e5fd2dd39d1b0f62d54.json
│   │   │   │   │   │   27d96b81cdd353d8ba277464751efff5d4c2d3c18ec2030e19dff8ea82ba95d5.json
│   │   │   │   │   │   26b19f10f0a8cdafbd812388d8131ea249416a6773333e97c6a31b3f43192188.json
│   │   │   │   │   │   26798ef0a18b5e8401998e0e98fcc7ccbe313a17bfe8a7d0abb95f95bb36eed1.json
│   │   │   │   │   │   90189329ec8a3ab02a1a817867b7730af3d20fb543e1ebd4138b8e457e932c93.json
│   │   │   │   │   │   604f014dc0bd920ff3e10b4c9f296c2813eb2a94f7048c45835aedcf1ebb66f8.json
│   │   │   │   │   │   d14f9799d51419cb9579b8753aef31983d27fae7933aa38fb8c4fb8677df54b6.json
│   │   │   │   │   │   5ed11964fcd31d0053253573721d1b68e5c7beb4d0e54c26918cbe9a92f10829.json
│   │   │   │   │   │   7e61999d3caede590296c122fffaea856c6d4938f2ba78358d4f5be188471986.json
│   │   │   │   │   │   46e747132ccd1e66878c38e1744225a16296d0fd3cf2395b27a7f03a76a14103.json
│   │   │   │   │   │   506d935a664f068bca5ee3b3eecde21173f1fd2d54ce176c92929f2a1aecd179.json
│   │   │   │   │   │   3fa48cb81866291ac748eb47e91719d7fb2830beeb6712e11d2c9abdab4e893f.json
│   │   │   │   │   │   ffe1eeb1088024b0397d900f12271b3b2f391505e8f2a06ab170d830b5c330d5.json
│   │   │   │   │   │   16091dbfed2095760ae9a42cd27583744858f953c81f4eef8bdc55f34e3ad36d.json
│   │   │   │   │   │   132c8136e8aa6d51cec785a2460beeacd68f7e2b437117dd6ed7b354a8f34049.json
│   │   │   │   │   │   54392e3252c0a57999446baa75b88bc5e3fb8ac41bb9eee84011eda55ef8991b.json
│   │   │   │   │   │   30c111b7857557d7df9c84fdc28e40ae5a54af2a2dd874f7b2a5b518d6d16fb0.json
│   │   │   │   │   │   f007d82dff335b4ca0c857a76a59d0eff0f32c426ab8101d2c68f2dfef0d0a22.json
│   │   │   │   │   │   854e0f782c03a667de51a28aaa6844279f5ebac487b62689474380b03a0b9ebe.json
│   │   │   │   │   │   141def7f000c2f016de543669e369582756a4fd3d718a963549d30fb50e9a3a2.json
│   │   │   │   │   │   8f6e3e84b0440d0812ac860c38a27c4fe506559c76edfe5dc41118068a6d0732.json
│   │   │   │   │   │   063d3c8ba2f8c4293f3a7fc20194de1786b9f1b4081f99ac299200c0a8be20a5.json
│   │   │   │   │   │   8274674351cfbd2b854ad86a0438be682884aec7143e88a68b74d563d5567477.json
│   │   │   │   │   │   ff8f3c8c90bce0bf0990733de874e72bb9b117e187ad896e65172f9d32f93226.json
│   │   │   │   │   │   fb77835aa6210e22c9b4c0f2768dfaf245de8942d8011e69bab46404d50f1b29.json
│   │   │   │   │   │   2579a1fc6502dc4d7a8323188b69867453a4ceb2fea71bb702c49b88cc3d5bad.json
│   │   │   │   │   │   2cc7434b222498578c1ff1cb2356a004157c14afef76e69ac2283b8f26ceb091.json
│   │   │   │   │   │   72a487adf9fdaa35b47435cf72e608f26198c0410262c1c0e1cd33218541d0bc.json
│   │   │   │   │   │   79f70848fc00f627cea74a9cc2a7c4a9969ff9232af7b091df531c76f547780d.json
│   │   │   │   │   │   8581fae6f5080df19b0b553053bc791b9a7edfc72afcc18c32d0c457f787c78e.json
│   │   │   │   │   │   b72de3029ff5287c73762a5870d4142bbcc11fcbf63473241f0c3c4f8de3129a.json
│   │   │   │   │   │   a18ac8a243e9452436f73bae0c6d9dc79402d69194e599b808aca69d1f22d5b9.json
│   │   │   │   │   │   6c6a1907d6784fdd263402fcce48ce6cd25f4b63bcb19bc6a0617ac4bc6d3525.json
│   │   │   │   │   │   11967a6822016fb7a03c416e2f3020550b057d6e5aa150741091c39bb218de3f.json
│   │   │   │   │   │   449f4f0d8dedcdda95535d08f198361e941736fad509a53c626bf3d8eac9b115.json
│   │   │   │   │   │   f97ff8beb2031f012a64d7abe940d3b5e588941f9655ab6611eba1466e5cb4d9.json
│   │   │   │   │   │   89738602eed04d9e59004f4187ba1d6d21da8666fe7412448c9f7eb0d11648d1.json
│   │   │   │   │   │   ea80e8bcc11589aeb3ed7bee3775c6700796a9f683cec67a7ceb226109c61c4a.json
│   │   │   │   │   │   913db14a18bea425740b0c82c9d5be26977a0290353f029bbafbb62b2c624374.json
│   │   │   │   │   │   0c6b68b1d5124d265c722f37c0da5af1367125eb62e760b892155df4826ef3dc.json
│   │   │   │   │   │   5f837dd2fdc5eda30807954f176832f8bbfa0f5d3e412bf9d8cb1f4cc12197f8.json
│   │   │   │   │   │   baccd17f5d5eb2c002a5b21e21f434b284b81858d39fe900c2b1a3bbc00199c3.json
│   │   │   │   │   │   5779aee8df72178d4e09922d0992b76cd11632bb2c98e32da6a65f84479d74a5.json
│   │   │   │   │   │   b5b720b4d0c0c1c04630310d11deea198727574eff6f8bbf7d53a94bd3943a10.json
│   │   │   │   │   │   d1d22d2274cfc09cd9d55146ba88bd93ef6105ed04c0d0c993985abffc04a9d8.json
│   │   │   │   │   │   f25a89a8d3287b1f97070e1244c26db42f8839a82a40e807a1fae68f623387c0.json
│   │   │   │   │   │   cda862cd5d475f43a2d9f01e94f1d6cdd8d9c07075373f63325874d8b93ee722.json
│   │   │   │   │   │   b205e606afce1080581c80344cba9f0232231a5b54fdecd650087df301b5e7f4.json
│   │   │   │   │   │   bbdd50ca5cd1059bfb72fd818b6284009f2af9994d3211d63fa8f474fe572539.json
│   │   │   │   │   │   fd01a1eb0ce0f5356ecefd3194d4ce7b32a3fcfd5a006af74cceb0ab8faf85fa.json
│   │   │   │   │   │   0fa814cbca29fde787e6033c3f06ad860a31070fc7bd559e4b959c8150f8e886.json
│   │   │   │   │   │   971d31cb7f6343b3c8933ecafb293d2351fd8606fff6cdf52c0c4f00f5d64998.json
│   │   │   │   │   │   fa09153953c71dbd951f68791591c9e15bb59c495e4d59201d9b95928fdd6f11.json
│   │   │   │   │   │   a83760c076fac5d776c5f6c8940821476822084bc12d4820edf901bf2b72e69f.json
│   │   │   │   │   │   a588c79e24da16d0e9706cdfa5196a6906651fcc1c21573bd90bc125505dce01.json
│   │   │   │   │   │   5319f9a491afc49a56408560bfb953c9d91024ace8caacb234f0bc319d3a50ee.json
│   │   │   │   │   │   01616c718fd2cf4e322a39db5af9f4ca9b306658b24625a0b5c5bde9f9cfb917.json
│   │   │   │   │   │   b72e95cafe996ea4307be1d3e58244ea7568ea685e95322212120224f2b24f21.json
│   │   │   │   │   │   357429456144e100747930379406937915bb334d07c1ec0ba43ff3a0e17f4096.json
│   │   │   │   │   │   83527d0995e31b5ef8fbf6249fcfdc030876818fe9fc894e49f1307f374a743e.json
│   │   │   │   │   │   0dd68fadb083d6a4da42dfdab3263905e11b611261cf960d446f75d4cf915901.json
│   │   │   │   │   │   d13b7d0777cc9d395f0e43cdca75f89f8dcc549de7034540919c8d3f7088bd8b.json
│   │   │   │   │   │   96e0b91149ddb6a7279ec7b13cbd9851a8dd453aa46ed2a11d02d9aecfe7c80c.json
│   │   │   │   │   │   1e807ef4afa4bdd97732ebb0701fedfaf57cdd19e1c708c8153d8b86b8cf02d8.json
│   │   │   │   │   │   ffd34e6bc97c1660b6ae653f53c90a8c4d226d4321e861597b702c851b81b9fb.json
│   │   │   │   │   │   0c7050cf18de1ce1678cad966f6b4651b85e5072ef1e58cb14b3ac1820ccfef7.json
│   │   │   │   │   │   2def14a95285b0691a06d3f615ff838f2c69f81e8abc88bfbbd863c62ab54ec0.json
│   │   │   │   │   │   051e9d956329ea128b1726846ba43f2c6290aaeea6f16cfac4361787b89010b8.json
│   │   │   │   │   │   b74cbf9eaf054eb9858d1a6a2d9faa667ad44ed47219be16f7a79008bf5d0417.json
│   │   │   │   │   │   661d798f61aab2fe0d39b9100c5566611236138df4a54fcad181ba3320da23a4.json
│   │   │   │   │   │   09d0f0501a111513e7362dffc58ac494f91cd32a08d1cb7317c3f90fc9d896c6.json
│   │   │   │   │   │   92a03d257297515dc72e9ff94a72a281a5b1c8a2887847eaf0f99010335df06f.json
│   │   │   │   │   │   a40b767a4a42a85380bd2fcc50839273c1fa00df19c12220e322a276311da14a.json
│   │   │   │   │   │   3cb0c0279e7ca1c40b2360604b984884f6b3a9f0623cfd24c7dff7f0eabd3ab7.json
│   │   │   │   │   │   835b776601af1ddf2bddb6e0a60899d022b4898e5b3300b2cffea19f76741025.json
│   │   │   │   │   │   c4c410fe5eb1b69a4ccf052362b0acbfee78e86d8eab542b094c03699ff649f8.json
│   │   │   │   │   │   7b3bcd68f90418929ec46c470d55b6a6393d0fd5a422f80b60f5623dc26b763c.json
│   │   │   │   │   │   94034c3ada028e501c9a906db2a749b1839432525316e274c293a1d84fea5eec.json
│   │   │   │   │   │   4a39673fe4a176f07a3fb660d87954f888831a8f69581be9948cfa12154cc5c7.json
│   │   │   │   │   │   ba2a6d97c58daee0df99e3948e69272368cde8f8e6ca96164bec437ea7a1de7a.json
│   │   │   │   │   │   fa2548fdf90ab37c793ea2669fc68b9f46f19f01ff516176024ba6fee5b44919.json
│   │   │   │   │   │   33b1d7b50930d306f91d4b773ab5d24517e4666da30d4100826a5e8394d2931e.json
│   │   │   │   │   │   e23bf8b08d25ed6e996e5c56085affd25162f3c2e2d0c39d2987c21f0806c58f.json
│   │   │   │   │   │   ff0171bb13d40f32dbf868c9a900b9c9cd447ab309d5c8658fcd0c5e385980fb.json
│   │   │   │   │   │   8ced539dbaabb60b17d29b20fe87d375542d6e4847c3e0342134a9a66425bca8.json
│   │   │   │   │   │   683b6f8f09ec442c39f92a4467eb8601c61294645aca536de0142133dc04cff4.json
│   │   │   │   │   │   e1b362b5523bd8bb2862ca9be6a005bcec273fd39dff0b4432b03afd49041205.json
│   │   │   │   │   │   ed723b14c841fa4cf0ae32fd0e199fb631cf6b42c5982c357fe11c682464ba9e.json
│   │   │   │   │   │   94ee3e12f6d7f1f520c4376bae9935eff41889b96090d0542f7afc8acc5a4c20.json
│   │   │   │   │   │   67d59a54738b821928d231897f3083d808d32d17bde3bc83988ea9c1fab0188a.json
│   │   │   │   │   │   049d310efa33ae4015adbfa4bfa28bb86f562966cf7e420784066ac0de3fdab1.json
│   │   │   │   │   │   72f8c66c332f784043839c066ceec4504b1d7a197ab3799d8c36a64712a486ab.json
│   │   │   │   │   │   7f3898e2a8f5f6f75245d551e1954fb46794168efc0cf9805860a672a5f10597.json
│   │   │   │   │   │   4f67a47aaad2e9454d9776270eff3785c2db985b8129793c31975a4571651a5d.json
│   │   │   │   │   │   30c12b154b450b990459642ad320b4e09fef5795d5acefe8df2f87a776551dcf.json
│   │   │   │   │   │   d1a0f952c3b232e30233ea6d73c4c41891242eefcb038c8236bcb95923188797.json
│   │   │   │   │   │   a76eca74c66d1b096963787b5a40342d8cccc16bfe75f41605a3978b3bfa465b.json
│   │   │   │   │   │   f279032cb967d97c3ea10d53ca9ef105ad73489c14580b547f9276d2e5592fe2.json
│   │   │   │   │   │   c5822aa9fb57649a4cc8f7336b19fe3086eaeca8f82926bee730e2419b3211cf.json
```

## 🛠️ Tecnologías

- **Backend:** Python · FastAPI · Uvicorn
- **LLM:** Ollama con `llama3.2:3b`
- **ML — Clasificación:** SVM (scikit-learn) + DistilBERT (Hugging Face Transformers)
- **ML — Predicción:** Regresión Polinómica grado 2 (scikit-learn)
- **Base de Datos:** SQLite
- **Frontend:** Angular 17+ (standalone components)
- **Excel:** XlsxWriter / Pandas

## 🚀 Instalación y Ejecución

### 1. Clonar el Repositorio

```bash
git clone https://github.com/FutilePanic82/PersonalFinancialTracker_SIC2025
cd PersonalFinancialTracker_SIC2025
```

### 2. Backend — Python

```bash
cd "Backend&Algorithms"
python -m venv venv
source venv/bin/activate        # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Instalar y ejecutar Ollama

```bash
# Instalar Ollama (https://ollama.com)
ollama pull llama3.2:3b
ollama serve                    # Dejar corriendo en otra terminal
```

### 4. Iniciar el Backend

```bash
cd "Backend&Algorithms"
uvicorn server:app --host 0.0.0.0 --port 8000 --reload
```

### 5. Frontend — Angular

```bash
cd chatbot-angular
npm install
ng serve                        # http://localhost:4200
```

## 📡 API Endpoints

| Método   | Ruta            | Descripción                                                       |
| -------- | --------------- | ----------------------------------------------------------------- |
| `POST`   | `/conversation` | Envía mensaje; extrae y clasifica transacciones automáticamente   |
| `GET`    | `/historial`    | Retorna todas las transacciones almacenadas                       |
| `POST`   | `/finalize`     | Genera y descarga archivo Excel                                   |
| `POST`   | `/predict`      | Predicción de gasto (regresión polinómica)                        |
| `POST`   | `/metas`        | Recibe distribución de presupuesto, devuelve consejo del asesor IA|
| `DELETE` | `/reset`        | Reinicia conversación en memoria                                  |

### Ejemplo — `/conversation`

**Request:**
```json
{
  "chat_history": [
    { "role": "user", "content": "Gasté $500 en comida y recibí $15000 de sueldo" }
  ]
}
```

**Response:**
```json
{
  "response": "He registrado tu gasto de $500 en comida y tu ingreso de $15,000.",
  "transacciones_detectadas": [
    { "concepto": "comida", "monto": 500, "categoria": "Alimentación", "tipo": "gasto" },
    { "concepto": "sueldo", "monto": 15000, "categoria": "Ingresos", "tipo": "ingreso" }
  ]
}
```

### Ejemplo — `/predict`

**Request:**
```json
{ "ingresos": 15000, "hijos": 1, "edad": 30, "educacion": 2 }
```

**Response:**
```json
{
  "gasto_predicho": 11250.50,
  "r2": 0.8724,
  "ahorro_estimado": 3749.50
}
```

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.


## 📊 Métricas de Pruebas Sintéticas

![Metrics Summary](Backend&Algorithms/metrics_summary.png)

> Generado automáticamente
