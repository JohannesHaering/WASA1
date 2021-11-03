import { TestBed } from '@angular/core/testing';

import { BackendtrainingserviceService } from './backendtrainingservice.service';

describe('BackendtrainingserviceService', () => {
  let service: BackendtrainingserviceService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(BackendtrainingserviceService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
