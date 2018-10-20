import {Injectable} from '@angular/core';
import {HttpClient, HttpHeaders} from '@angular/common/http';
import {Observable} from 'rxjs/internal/Observable';
import {environment} from '../../environments/environment';

@Injectable()
export class TransportService {
  constructor(private http: HttpClient) {}

  get(relativeUrl, headers = new HttpHeaders({'Content-Type': 'application/json'}), params?): Observable<any> {
    return this.http.get(this.getUrl(relativeUrl), {headers: headers, params});
  }

  post(relativeUrl, data, headers = new HttpHeaders({'Content-Type': 'application/json'})): Observable<any> {
    return this.http.post(this.getUrl(relativeUrl), data, {headers});
  }

  private getUrl(url): string {
    return `${environment.baseUrl}${environment.prefix}${url}`;
  }
}
