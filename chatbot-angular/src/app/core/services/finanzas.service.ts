import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Transaccion {
    id: number;
    fecha: string;
    concepto: string;
    monto: number;
    categoria: string;
    tipo: 'ingreso' | 'gasto';
}

export interface ConversationResponse {
    response: string;
    transacciones_detectadas: Transaccion[];
}

export interface PredictRequest {
    ingresos: number;
    hijos: number;
    edad: number;
    educacion: number;
}

export interface PredictResponse {
    gasto_predicho: number;
    r2: number;
    ahorro_estimado: number;
}

@Injectable({ providedIn: 'root' })
export class FinanzasService {
    private readonly api = 'http://localhost:8000';

    constructor(private http: HttpClient) { }

    /** Send a user message; backend detects and saves transactions */
    sendConversation(chatHistory: any[]): Observable<ConversationResponse> {
        return this.http.post<ConversationResponse>(
            `${this.api}/conversation`,
            { chat_history: chatHistory }
        );
    }

    /** Download the Excel file of all saved transactions */
    finalize(): Observable<Blob> {
        return this.http.post(
            `${this.api}/finalize`,
            {},
            { responseType: 'blob' }
        );
    }

    /** Get all stored transactions */
    getHistorial(): Observable<{ transacciones: Transaccion[] }> {
        return this.http.get<{ transacciones: Transaccion[] }>(`${this.api}/historial`);
    }

    /** Polynomial regression spending prediction */
    predict(data: PredictRequest): Observable<PredictResponse> {
        return this.http.post<PredictResponse>(`${this.api}/predict`, data);
    }

    /** LLM advice on budget distribution */
    metasAdvice(metas: { nombre: string; valor: number }[]): Observable<{ response: string }> {
        return this.http.post<{ response: string }>(`${this.api}/metas`, { metas });
    }

    resetChat(): Observable<any> {
        return this.http.delete(`${this.api}/reset`);
    }

    /** Get list of generated reports */
    getReportes(): Observable<Reporte[]> {
        return this.http.get<Reporte[]>(`${this.api}/reportes`);
    }

    /** Download a specific report by ID */
    downloadReport(id: number): Observable<Blob> {
        return this.http.get(`${this.api}/reportes/${id}/download`, { responseType: 'blob' });
    }
}

export interface Reporte {
    id: number;
    fecha: string;
    nombre: string;
    path: string;
}
