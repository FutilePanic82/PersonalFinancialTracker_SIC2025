import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MetasFinancierasComponent } from './metas-financieras.component';

describe('MetasFinancierasComponent', () => {
  let component: MetasFinancierasComponent;
  let fixture: ComponentFixture<MetasFinancierasComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [MetasFinancierasComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(MetasFinancierasComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
