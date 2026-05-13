import { TestBed } from '@angular/core/testing';
import {
  HttpClientTestingModule,
  HttpTestingController,
} from '@angular/common/http/testing';
import { Observable } from 'rxjs';

import { FinanzasService, Transaccion, ConversationResponse, PredictRequest, PredictResponse } from './finanzas.service';

describe('FinanzasService', () => {
  let service: FinanzasService;
  let httpMock: HttpTestingController;

  const API = 'http://localhost:8000';

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [FinanzasService],
    });
    service = TestBed.inject(FinanzasService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  describe('sendConversation', () => {
    it('should POST to /conversation with chat_history', (done) => {
      const mockResponse: ConversationResponse = {
        response: 'Respuesta de prueba',
        transacciones_detectadas: [],
      };
      const payload = [{ role: 'user', content: 'Hola' }];

      service.sendConversation(payload).subscribe((res) => {
        expect(res).toEqual(mockResponse);
        done();
      });

      const req = httpMock.expectOne(`${API}/conversation`);
      expect(req.request.method).toBe('POST');
      expect(req.request.body).toEqual({ chat_history: payload });
      req.flush(mockResponse);
    });
  });

  describe('getHistorial', () => {
    it('should GET /historial and return transacciones', (done) => {
      const mockTransacciones: Transaccion[] = [
        { id: 1, fecha: '2026-05-13', concepto: 'Comida', monto: 500, categoria: 'Alimentación', tipo: 'gasto' },
      ];

      service.getHistorial().subscribe((res) => {
        expect(res.transacciones).toEqual(mockTransacciones);
        done();
      });

      const req = httpMock.expectOne(`${API}/historial`);
      expect(req.request.method).toBe('GET');
      req.flush({ transacciones: mockTransacciones });
    });
  });

  describe('predict', () => {
    it('should POST to /predict with request data', (done) => {
      const mockResponse: PredictResponse = {
        gasto_predicho: 25000,
        r2: 0.85,
        ahorro_estimado: 5000,
      };
      const payload: PredictRequest = {
        ingresos: 50000,
        hijos: 2,
        edad: 35,
        educacion: 3,
      };

      service.predict(payload).subscribe((res) => {
        expect(res).toEqual(mockResponse);
        done();
      });

      const req = httpMock.expectOne(`${API}/predict`);
      expect(req.request.method).toBe('POST');
      expect(req.request.body).toEqual(payload);
      req.flush(mockResponse);
    });
  });

  describe('finalize', () => {
    it('should POST to /finalize and return blob', (done) => {
      const blobData = new Uint8Array([80, 75, 3, 4]);
      const blob = new Blob([blobData], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });

      service.finalize().subscribe((res) => {
        expect(res).toBeInstanceOf(Blob);
        done();
      });

      const req = httpMock.expectOne(`${API}/finalize`);
      expect(req.request.method).toBe('POST');
      req.flush(blob);
    });
  });

  describe('resetChat', () => {
    it('should DELETE /reset', (done) => {
      service.resetChat().subscribe((res) => {
        expect(res).toBeDefined();
        done();
      });

      const req = httpMock.expectOne(`${API}/reset`);
      expect(req.request.method).toBe('DELETE');
      req.flush({});
    });
  });

  describe('getReportes', () => {
    it('should GET /reportes', (done) => {
      const mockReportes = [
        { id: 1, fecha: '2026-05-13', nombre: 'Reporte Mayo', path: '/reports/reporte.xlsx' },
      ];

      service.getReportes().subscribe((res) => {
        expect(res).toEqual(mockReportes);
        done();
      });

      const req = httpMock.expectOne(`${API}/reportes`);
      expect(req.request.method).toBe('GET');
      req.flush(mockReportes);
    });
  });

  describe('metasAdvice', () => {
    it('should POST to /metas with metas array', (done) => {
      const payload = [{ nombre: 'Ahorro', valor: 10000 }];
      const mockResponse = { response: 'Te recomiendo ahorrar el 20%' };

      service.metasAdvice(payload).subscribe((res) => {
        expect(res).toEqual(mockResponse);
        done();
      });

      const req = httpMock.expectOne(`${API}/metas`);
      expect(req.request.method).toBe('POST');
      expect(req.request.body).toEqual({ metas: payload });
      req.flush(mockResponse);
    });
  });
});