import {Composition} from 'remotion';
import {DURACAO_03, Fluxo03} from './cenas/03_fluxo';
import {Alcance05, DURACAO_05} from './cenas/05_alcance';
import {DURACAO_06, Funil06} from './cenas/06_funil';
import {DURACAO_09, Revisor09} from './cenas/09_revisor';

// Ids com hífen (o Remotion não aceita "_" em id): 03-fluxo = cena 03_fluxo.
// Cenas do roteiro com "ferramenta": "remotion". Durações = tempos.json (quadros a 30 fps).
export const Root = () => (
  <>
    <Composition id="03-fluxo" component={Fluxo03} durationInFrames={DURACAO_03} fps={30} width={1920} height={1080} />
    <Composition id="05-alcance" component={Alcance05} durationInFrames={DURACAO_05} fps={30} width={1920} height={1080} />
    <Composition id="06-funil" component={Funil06} durationInFrames={DURACAO_06} fps={30} width={1920} height={1080} />
    <Composition id="09-revisor" component={Revisor09} durationInFrames={DURACAO_09} fps={30} width={1920} height={1080} />
  </>
);
